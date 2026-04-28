from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import PyPDF2
import io
import requests
from app.database import init_db, SessionLocal, Documento
from fastapi.middleware.cors import CORSMiddleware

"""
API Juridiquês Zero - Backend Principal.
Desenvolvido com FastAPI, este serviço gerencia a extração de texto de PDFs,
a comunicação com o modelo de IA local (Ollama) e a persistência de dados.
"""

# Inicializa o banco de dados (cria as tabelas se não existirem)
init_db()

app = FastAPI(
    title="Juridiquês Zero API",
    description="API para simplificação de termos jurídicos usando IA local.",
    version="1.0.0"
)

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite que a interface Streamlit (ou outros frontends) se comunique com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def traduzir_com_ia_local(texto):
    """
    Envia o texto extraído para o motor de IA local (Ollama) rodando o modelo Phi-3.

    Args:
        texto (str): O texto jurídico bruto a ser simplificado.

    Returns:
        str: O resumo simplificado gerado pela IA ou mensagem de erro.
    """
    url_ollama = "http://ollama:11434/api/generate"

    # Prompt estruturado para guiar a IA na geração da resposta
    prompt_gerado = (
        "Você é um tradutor jurídico. Converta o texto abaixo em linguagem simples.\n\n"
        "Siga este formato:\n"
        "TÍTULO: [Nome do Processo]\n"
        "RESUMO SIMPLIFICADO: [Explicação curta do que aconteceu]\n"
        "AÇÕES NECESSÁRIAS: [O que precisa ser feito agora]\n\n"
        f"TEXTO ORIGINAL:\n{texto[:1200]}" # Limite de caracteres para performance na CPU
    )

    payload = {
        "model": "phi3",
        "prompt": prompt_gerado,
        "stream": False,
        "options": {
            "temperature": 0.2,      # Menor temperatura = respostas mais focadas e menos criativas
            "num_predict": 450,      # Limite de tokens na resposta
            "repeat_penalty": 1.1,   # Penalidade para evitar repetições de palavras
            "stop": ["TEXTO ORIGINAL", "###", "Instrução:"] # Marcadores de parada
        }
    }
    
    try:
        # Timeout longo devido ao processamento local em CPU (PoC)
        response = requests.post(url_ollama, json=payload, timeout=300)
        return response.json().get("response", "IA não retornou resposta.")
    except Exception as e:
        return f"Erro na conexão com IA Local: {e}"

# --- ROTAS DA API ---

@app.get("/", tags=["Health"])
def home():
    """Rota raiz para verificar se a API está online."""
    return {"status": "API Online"}

@app.post("/upload", tags=["Processamento"])
async def upload_pdf(file: UploadFile = File(...), x_api_key: str = Header(None)):
    """
    Recebe um arquivo PDF, extrai seu texto e solicita a tradução para a IA.
    Os dados são salvos no PostgreSQL ao final.
    """
    # Verificação simples de chave de API para segurança básica
    if x_api_key != "Juridiques2026":
        raise HTTPException(status_code=403, detail="Chave Inválida")

    content = ""
    # 2. Extração de texto do PDF
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(await file.read()))
        for page in pdf_reader.pages:
            content += page.extract_text() or ""
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler PDF: {e}")

    # 3. Chamada do motor de IA Local (Ollama)
    traducao_ia = traduzir_com_ia_local(content)

    # 4. Persistência no Banco de Dados
    db = SessionLocal()
    try:
        novo_doc = Documento(
            nome_arquivo=file.filename,
            categoria="Jurídico",
            conteudo_extraido=content
        )
        db.add(novo_doc)
        db.commit()
        db.refresh(novo_doc)
    except Exception as e:
        db.rollback()
        print(f"ERRO ao salvar no banco: {e}")
    finally:
        db.close()

    # 5. Retorno com o texto bruto e a tradução da IA
    return {
        "content": content, 
        "traducao": traducao_ia, 
        "status": "salvo_no_banco"
    }

@app.get("/documentos", tags=["Consultas"])
def listar_documentos(busca: str = None):
    """
    Lista os documentos salvos no banco de dados, com opção de busca por nome.
    """
    db = SessionLocal()
    try:
        query = db.query(Documento)
        if busca:
            # Filtro insensível a maiúsculas/minúsculas (LIKE)
            query = query.filter(Documento.nome_arquivo.ilike(f"%{busca}%"))
        documentos = query.all()
        return documentos
    finally:
        db.close()
