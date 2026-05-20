import aiohttp
import asyncio
import hashlib
import json
import redis
import time
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ResultadoIA:
    resumo: str
    prazos: list
    acoes: list
    modelo: str
    tempo_ms: int
    tokens_entrada: int
    tokens_saida: int
    cache_hit: bool = False
    erro: Optional[str] = None

class MotorIA:
    MODELOS_LOCAL = {
        "primario": "gemma2:2b",
        "secundario": "llama3.1",
    }
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    TIMEOUT_LOCAL = 180
    TIMEOUT_GEMINI = 30
    
    def __init__(self, ollama_url: str = "http://ollama:11434", redis_url: str = "redis://redis:6379/0"):
        self.ollama_url = ollama_url
        self.cache = redis.Redis.from_url(redis_url, decode_responses=True)
        self.modelo_padrao = self.MODELOS_LOCAL["primario"]
        
        self.system_prompt = """Voce e um assistente juridico brasileiro. 
Simplifique o texto em linguagem clara. 
Estrutura obrigatoria:
RESUMO: (max 3 frases)
PRAZOS: (lista com datas)
ACOES: (o que fazer)"""
    
    def _gerar_hash(self, texto: str) -> str:
        return hashlib.sha256(texto.encode('utf-8')).hexdigest()[:16]
    
    def _verificar_cache(self, texto_hash: str) -> Optional[ResultadoIA]:
        try:
            cached = self.cache.get(f"ia:{texto_hash}")
            if cached:
                data = json.loads(cached)
                return ResultadoIA(**data, cache_hit=True)
        except Exception as e:
            logger.warning(f"Erro no cache: {e}")
        return None
    
    def _salvar_cache(self, texto_hash: str, resultado: ResultadoIA, ttl: int = 86400):
        try:
            data = asdict(resultado)
            data.pop('cache_hit', None)
            self.cache.setex(f"ia:{texto_hash}", ttl, json.dumps(data))
        except Exception as e:
            logger.warning(f"Erro ao salvar cache: {e}")
    
    def _extrair_estruturado(self, texto_raw: str) -> Dict[str, Any]:
        linhas = texto_raw.split('\n')
        resumo = []
        prazos = []
        acoes = []
        secao_atual = "resumo"
        
        for linha in linhas:
            linha_limpa = linha.strip().upper()
            
            if "PRAZO" in linha_limpa and ":" in linha_limpa:
                secao_atual = "prazos"
                continue
            elif "ACAO" in linha_limpa or "ACAO" in linha_limpa:
                secao_atual = "acoes"
                continue
            elif "RESUMO" in linha_limpa:
                secao_atual = "resumo"
                continue
            
            if linha.strip() and not linha.strip().startswith('-'):
                if secao_atual == "resumo":
                    resumo.append(linha.strip())
                elif secao_atual == "prazos":
                    prazos.append(linha.strip().lstrip('- '))
                elif secao_atual == "acoes":
                    acoes.append(linha.strip().lstrip('- '))
        
        return {
            "resumo": " ".join(resumo) if resumo else texto_raw[:500],
            "prazos": prazos,
            "acoes": acoes
        }
    
    async def _chamar_ollama(self, prompt: str, modelo: str, timeout: int = None) -> Optional[Dict]:
        timeout = timeout or self.TIMEOUT_LOCAL
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": modelo,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.15,
                            "num_predict": 800,
                            "top_k": 30,
                            "top_p": 0.85,
                            "repeat_penalty": 1.1,
                        }
                    },
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as response:
                    
                    if response.status != 200:
                        logger.error(f"Ollama erro HTTP {response.status}")
                        return None
                    
                    return await response.json()
                    
            except asyncio.TimeoutError:
                logger.warning(f"Timeout Ollama ({timeout}s)")
                return None
            except Exception as e:
                logger.error(f"Erro Ollama: {e}")
                return None
    
    async def _chamar_gemini(self, prompt: str) -> Optional[Dict]:
        if not self.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY nao configurada")
            return None
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.GEMINI_URL}?key={self.GEMINI_API_KEY}",
                    json={
                        "contents": [{
                            "parts": [{
                                "text": f"{self.system_prompt}\n\n{prompt}"
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.15,
                            "maxOutputTokens": 800,
                            "topP": 0.85,
                        }
                    },
                    timeout=aiohttp.ClientTimeout(total=self.TIMEOUT_GEMINI)
                ) as response:
                    
                    if response.status != 200:
                        logger.error(f"Gemini erro HTTP {response.status}")
                        return None
                    
                    data = await response.json()
                    
                    if "candidates" in data and len(data["candidates"]) > 0:
                        texto = data["candidates"][0]["content"]["parts"][0]["text"]
                        return {"response": texto}
                    
                    return None
                    
            except asyncio.TimeoutError:
                logger.warning(f"Timeout Gemini ({self.TIMEOUT_GEMINI}s)")
                return None
            except Exception as e:
                logger.error(f"Erro Gemini: {e}")
                return None
    
    async def processar(self, texto: str, tipo_documento: str = "geral", usar_gemini: bool = False) -> ResultadoIA:
        inicio = time.time()
        texto_hash = self._gerar_hash(texto)
        
        cached = self._verificar_cache(texto_hash)
        if cached:
            logger.info(f"Cache hit! Tempo: 0ms")
            return cached

        texto_truncado = texto[:6000]
        prompt = f"{self.system_prompt}\n\nTEXTO JURIDICO:\n{texto_truncado}\n\nSIMPLIFICACAO:"
        
        resposta_raw = None
        modelo_usado = None
        tokens_info = {"prompt": len(texto_truncado.split()), "response": 0}
        
        if usar_gemini and self.GEMINI_API_KEY:
            logger.info("Tentando Gemini...")
            resultado_gemini = await self._chamar_gemini(prompt)
            
            if resultado_gemini and "response" in resultado_gemini:
                resposta_raw = resultado_gemini["response"]
                modelo_usado = "gemini-2.0-flash"
                tokens_info["response"] = len(resposta_raw.split())
                logger.info("Sucesso com Gemini!")
        
        if not resposta_raw:
            modelos_tentativa = [
                self.MODELOS_LOCAL["primario"],
                self.MODELOS_LOCAL["secundario"],
            ]
            
            for modelo in modelos_tentativa:
                logger.info(f"Tentando modelo local: {modelo}")
                resultado = await self._chamar_ollama(prompt, modelo)
                
                if resultado and "response" in resultado:
                    resposta_raw = resultado["response"]
                    modelo_usado = modelo
                    tokens_info["response"] = len(resposta_raw.split())
                    logger.info(f"Sucesso com {modelo}")
                    break
        
        if resposta_raw:
            estruturado = self._extrair_estruturado(resposta_raw)
            
            resultado = ResultadoIA(
                resumo=estruturado["resumo"],
                prazos=estruturado["prazos"],
                acoes=estruturado["acoes"],
                modelo=modelo_usado,
                tempo_ms=int((time.time() - inicio) * 1000),
                tokens_entrada=tokens_info["prompt"],
                tokens_saida=tokens_info["response"],
                cache_hit=False
            )
        else:
            resultado = ResultadoIA(
                resumo="Nao foi possivel processar este documento automaticamente. Recomendamos revisao manual.",
                prazos=[],
                acoes=["Revisar documento manualmente"],
                modelo="fallback",
                tempo_ms=int((time.time() - inicio) * 1000),
                tokens_entrada=0,
                tokens_saida=0,
                erro="Todos os modelos falharam ou timeout"
            )
        
        self._salvar_cache(texto_hash, resultado)
        return resultado
    
    async def health_check(self) -> Dict[str, Any]:
        status = {
            "ollama_online": False,
            "modelos_disponiveis": [],
            "gemini_configurado": bool(self.GEMINI_API_KEY),
            "redis_online": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_url}/api/tags", timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        status["ollama_online"] = True
                        status["modelos_disponiveis"] = [m["name"] for m in data.get("models", [])]
        except:
            pass
        
        try:
            self.cache.ping()
            status["redis_online"] = True
        except:
            pass
        
        return status
