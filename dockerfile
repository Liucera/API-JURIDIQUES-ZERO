# Estágio Único: Python 3.12 (Slim para menor tamanho de imagem)
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instalação das dependências
# Copiamos primeiro apenas o requirements para aproveitar o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do projeto para o diretório de trabalho
COPY . .

# Expõe as portas utilizadas pelas aplicações
# 8000: FastAPI (Backend)
# 8501: Streamlit (Frontend)
EXPOSE 8000
EXPOSE 8501

# O comando de inicialização é definido no docker-compose.yml para permitir
# flexibilidade entre os serviços de API e Interface.
