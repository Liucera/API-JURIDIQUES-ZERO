import io
from typing import Optional
import PyPDF2
import logging

logger = logging.getLogger(__name__)

async def extrair_texto_pdf(conteudo: bytes) -> str:
    try:
        pdf_file = io.BytesIO(conteudo)
        reader = PyPDF2.PdfReader(pdf_file)
        
        texto = []
        for i, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    texto.append(page_text)
            except Exception as e:
                logger.warning(f"Erro na pagina {i}: {e}")
                continue
        
        resultado = "\n".join(texto)
        import re
        resultado = re.sub(r'\s+', ' ', resultado).strip()
        
        return resultado[:15000]
        
    except Exception as e:
        logger.error(f"Erro ao extrair PDF: {e}")
        return ""
