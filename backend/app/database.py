import asyncpg
import os
from typing import List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:Juridiques2026@db:5432/juridiques_zero")

class Database:
    def __init__(self):
        self.pool = None
    
    async def _get_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
        return self.pool
    
    async def health_check(self) -> bool:
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def salvar_documento(
        self,
        nome_arquivo: str,
        tipo: str,
        texto_original: str,
        resumo: str,
        modelo_ia: str,
        tempo_ms: int,
        cache: bool = False,
        prazos: List[str] = None,
        acoes: List[str] = None
    ) -> int:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO documentos 
                (nome_arquivo, tipo, texto_original, resumo, prazos, acoes, modelo_ia, tempo_ms, cache_hit, processado_em)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW())
                RETURNING id
                """,
                nome_arquivo,
                tipo,
                texto_original,
                resumo,
                json.dumps(prazos or []),
                json.dumps(acoes or []),
                modelo_ia,
                tempo_ms,
                cache
            )
            return row["id"]
    
    async def listar_documentos(self, limit: int = 50) -> List[Dict]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, nome_arquivo, tipo, resumo, modelo_ia, tempo_ms, cache_hit, criado_em
                FROM documentos
                ORDER BY criado_em DESC
                LIMIT $1
                """,
                limit
            )
            return [dict(r) for r in rows]
    
    async def contar_documentos(self) -> int:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM documentos")
    
    async def tempo_medio_processamento(self) -> int:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT COALESCE(AVG(tempo_ms), 0)::int FROM documentos WHERE criado_em > NOW() - INTERVAL '30 days'"
            )
    
    async def taxa_cache(self) -> float:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM documentos WHERE criado_em > NOW() - INTERVAL '7 days'")
            if total == 0:
                return 0.0
            hits = await conn.fetchval(
                "SELECT COUNT(*) FROM documentos WHERE cache_hit = TRUE AND criado_em > NOW() - INTERVAL '7 days'"
            )
            return hits / total
    
    async def modelos_mais_usados(self) -> Dict[str, int]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT modelo_ia, COUNT(*) as total
                FROM documentos
                WHERE criado_em > NOW() - INTERVAL '30 days'
                GROUP BY modelo_ia
                ORDER BY total DESC
                """
            )
            return {r["modelo_ia"]: r["total"] for r in rows}
