FROM python:3.12-slim

# Define onde o código vai morar dentro do contêiner
WORKDIR /app

# Copia as dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIA TUDO da sua pasta para dentro do /app do contêiner
COPY . .

# Expõe as portas
EXPOSE 8000
EXPOSE 8501

# O comando de execução (garantindo que ele aponte para os arquivos certos)
# Note que não precisamos de caminhos longos aqui porque estamos no WORKDIR /app
