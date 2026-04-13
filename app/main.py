from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from pypdf import PdfReader
import os

app = FastAPI()

@app.get("/")
def home():
    # O comando abaixo precisa de 4 espaços de recuo
    return {"mensagem": "API Juridiquês Zero rodando"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), x_api_key: str = Header(...)):
    # 1. Validação de Chave (O Portão Principal) 🔑
    if x_api_key != "Juridiques2026":
        raise HTTPException(status_code=401, detail="A senha está incorreta")

    # 2. Validação de Tipo 📄
   if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo enviado não é um PDF válido.")

    # 3. Validação de Tamanho (A Balança) ⚖️
    MAX_FILE_SIZE = 15 * 1024 * 1024
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Tamanho máximo permitido é de 15Mb")

    # --- SÓ CHEGA AQUI SE PASSAR NAS 3 ETAPAS ACIMA ---
    temp_path = f"/tmp/{file.filename}"
    
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Ler PDF 📖
    reader = PdfReader(temp_path)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() or ""

    # Simulação de "tradução" 💡
    texto_simplificado = f"VERSÃO SIMPLIFICADA:\n\n{texto[:1000]}"

    # Deletar arquivo temporário 🧹
    os.remove(temp_path)

    return {"resultado": texto_simplificado}
