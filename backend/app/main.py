from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.ia_engine import MotorIA
from app.database import Database
from app.pdf_extractor import extrair_texto_pdf

app = FastAPI(
    title="Juridiques Zero API",
    description="Simplificacao de documentos juridicos - IA Hibrida",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ia = MotorIA()
db = Database()

class PromptRequest(BaseModel):
    texto: str
    tipo: Optional[str] = "geral"
    usar_gemini: Optional[bool] = False

class UploadResponse(BaseModel):
    id: int
    status: str
    resumo: Optional[str] = None
    prazos: list = []
    acoes: list = []
    tempo_ms: int = 0
    modelo: str = ""
    cache: bool = False

@app.get("/")
async def root():
    return {
        "nome": "Juridiques Zero",
        "versao": "2.1.0",
        "ia": "Hibrida (Ollama + Gemini)",
        "custo_ia": "Variavel (Gemini: pago | Ollama: gratis)"
    }

@app.get("/health")
async def health():
    ia_status = await ia.health_check()
    db_status = await db.health_check()
    
    return {
        "status": "ok" if db_status else "degraded",
        "ia": ia_status,
        "database": db_status
    }

@app.post("/simplificar", response_model=UploadResponse)
async def simplificar_texto(request: PromptRequest):
    if not request.texto or len(request.texto.strip()) < 50:
        raise HTTPException(400, "Texto muito curto. Minimo 50 caracteres.")
    
    resultado = await ia.processar(request.texto, request.tipo, request.usar_gemini)
    
    doc_id = await db.salvar_documento(
        nome_arquivo="prompt_direto",
        tipo="prompt",
        texto_original=request.texto[:1000],
        resumo=resultado.resumo,
        modelo_ia=resultado.modelo,
        tempo_ms=resultado.tempo_ms,
        cache=resultado.cache_hit,
        prazos=resultado.prazos,
        acoes=resultado.acoes
    )
    
    return UploadResponse(
        id=doc_id,
        status="concluido" if not resultado.erro else "parcial",
        resumo=resultado.resumo,
        prazos=resultado.prazos,
        acoes=resultado.acoes,
        tempo_ms=resultado.tempo_ms,
        modelo=resultado.modelo,
        cache=resultado.cache_hit
    )

@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...), usar_gemini: bool = False):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Apenas arquivos PDF sao aceitos.")
    
    conteudo = await file.read()
    texto = await extrair_texto_pdf(conteudo)
    
    if not texto or len(texto.strip()) < 100:
        raise HTTPException(400, "PDF vazio ou sem texto extraivel.")
    
    resultado = await ia.processar(texto, "pdf", usar_gemini)
    
    doc_id = await db.salvar_documento(
        nome_arquivo=file.filename,
        tipo="pdf",
        texto_original=texto[:2000],
        resumo=resultado.resumo,
        modelo_ia=resultado.modelo,
        tempo_ms=resultado.tempo_ms,
        cache=resultado.cache_hit,
        prazos=resultado.prazos,
        acoes=resultado.acoes
    )
    
    return UploadResponse(
        id=doc_id,
        status="concluido",
        resumo=resultado.resumo,
        prazos=resultado.prazos,
        acoes=resultado.acoes,
        tempo_ms=resultado.tempo_ms,
        modelo=resultado.modelo,
        cache=resultado.cache_hit
    )

@app.get("/documentos")
async def listar_documentos(limit: int = 50):
    return await db.listar_documentos(limit)

@app.get("/metricas")
async def metricas():
    return {
        "total_documentos": await db.contar_documentos(),
        "tempo_medio": await db.tempo_medio_processamento(),
        "taxa_cache": await db.taxa_cache(),
        "modelos_mais_usados": await db.modelos_mais_usados(),
        "gemini_disponivel": bool(ia.GEMINI_API_KEY)
    }
