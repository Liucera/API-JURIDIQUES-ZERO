from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import PyPDF2
import io

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

# Permite que o site (Streamlit) fale com a API sem bloqueios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # 3. Mostra no terminal para você conferir (Plaintext)
    print(f"DEBUG - Texto extraído: {content[:500]}...") 

    # 4. Retorna para o Streamlit
    return {"content": content}
