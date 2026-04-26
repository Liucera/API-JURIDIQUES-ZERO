from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import PyPDF2
import io
import requests  # NOVO: Para falar com o Ollama
from app.database import init_db

# Inicializa o banco
init_db()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FUNÇÃO AUXILIAR DA IA LOCAL ---
def traduzir_com_ia_local(texto):
    url_ollama = "http://ollama:11434/api/generate"

    # Reduzimos drasticamente as instruções para o Phi-3 focar no texto
    prompt_gerado = (
        "Você é um tradutor jurídico. Converta o texto abaixo em linguagem simples.\n\n"
        "Siga este formato:\n"
        "TÍTULO: [Nome do Processo]\n"
        "RESUMO SIMPLIFICADO: [Explicação curta do que aconteceu]\n"
        "AÇÕES NECESSÁRIAS: [O que precisa ser feito agora]\n\n"
        f"TEXTO ORIGINAL:\n{texto[:1200]}" # Limitamos o texto para evitar lentidão
    )

    payload = {
        "model": "phi3",
        "prompt": prompt_gerado,
        "stream": False,
        "options": {
            "temperature": 0.2,      # Subimos levemente para ele concluir frases de forma mais natural
            "num_predict": 450,      # Aumentamos o limite de palavras para ele não ser cortado
            "repeat_penalty": 1.1,   # Suavizamos a penalidade para ele não travar
            "stop": ["TEXTO ORIGINAL", "###", "Instrução:"] # Mantemos apenas as travas estruturais
        }
    }
    
    # Mantenha o seu código de requests abaixo...

    # Resto do seu código de requests...
    try:
        response = requests.post(url_ollama, json=payload, timeout=300) # Aumentei o timeout para o Llama 3
        return response.json().get("response", "IA não retornou resposta.")
    except Exception as e:
        return f"Erro na conexão com IA Local: {e}"

# --- ROTAS ---

@app.get("/")
def home():
    return {"status": "API Online"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), x_api_key: str = Header(None)):
    # 1. Verifica sua senha pessoal
    if x_api_key != "Juridiques2026":
        raise HTTPException(status_code=403, detail="Chave Inválida")

    content = ""
    # 2. Lê o PDF
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(await file.read()))
    for page in pdf_reader.pages:
        content += page.extract_text() or ""

    # 3. CHAMADA DA IA LOCAL (Ollaminha entrando em ação)
    traducao_ia = traduzir_com_ia_local(content)

    # 4. Salva no Banco de Dados
    from app.database import SessionLocal, Documento
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
        print(f"DEBUG - Documento salvo no banco com ID: {novo_doc.id}")
    except Exception as e:
        print(f"ERRO ao salvar no banco: {e}")
        db.rollback()
    finally:
        db.close()

    # 5. Retorna para o Streamlit (agora com a tradução!)
    return {
        "content": content, 
        "traducao": traducao_ia, 
        "status": "salvo_no_banco"
    }

@app.get("/documentos")
def listar_documentos(busca: str = None):
    from app.database import SessionLocal, Documento
    db = SessionLocal()
    try:
        query = db.query(Documento)
        if busca:
            query = query.filter(Documento.nome_arquivo.ilike(f"%{busca}%"))
        documentos = query.all()
        return documentos
    finally:
        db.close()
