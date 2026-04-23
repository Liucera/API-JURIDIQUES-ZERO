ATUALIZAÇÃO DO PROJETO (VERSÃO DOCKER)
# ⚖️ Juridiques Zero - Arquitetura Conteinerizada

Este projeto foi evoluído para uma arquitetura de microserviços utilizando Docker, permitindo o provisionamento rápido e isolado de todo o ecossistema.

## 🏗️ Arquitetura do Sistema
O sistema foi desenhado para rodar em contêineres separados, garantindo escalabilidade e segurança:

1. **API Backend (FastAPI)**: Responsável pelo motor de extração de dados e processamento de PDFs.
2. **Interface Frontend (Streamlit)**: Porta de entrada para o usuário, gerenciando a comunicação com a API e com a IA.

## 🐳 Docker e Provisionamento
Utilizamos o **Docker Compose** para orquestrar os serviços. A comunicação entre os contêineres é feita através de uma rede interna, onde a Interface localiza a API pelo nome de serviço `http://api:8000`.

### Como rodar:
1. Certifique-se de ter o Docker instalado.
2. Crie um arquivo `.env` com suas chaves de API.
3. Execute: `docker-compose up --build`

## 📸 Demonstração e Documentação
Confira abaixo os detalhes da arquitetura e do funcionamento do sistema:

![Arquitetura do Sistema](./docs/imagem7.jpg) 
*(Dica: Escolha a melhor imagem para ser a principal)*

> [!TIP]
> Você pode encontrar o detalhamento técnico completo no arquivo [Projeto Juridiquês Zero API.pdf](./docs/Projeto%20Juridiquês%20Zero%20API.pdf).

______________________________________________________________________________________________________________________________________________________________________________________________________________________+
# ⚖️ API Juridiques Zero (PROJETO INICIAL)

Uma solução inteligente para desmistificar o "juridiquês", automatizando a extração de dados críticos e a análise de documentos judiciais.

## 🚀 Sobre o Projeto
Esta API foi desenvolvida para transformar documentos jurídicos complexos em informações acionáveis. Utilizando a arquitetura moderna do FastAPI e PyMuPDF, ela garante precisão na leitura de metadados e textos de processos.

---

## 🔐 Segurança e Autenticação
A API está protegida por uma chave de segurança. Para realizar requisições aos endpoints, você deve incluir o seguinte cabeçalho (Header):

- **Header Key:** `x-api-key`
- **Valor Padrão:** `Juridiques2026`

---

## 📸 Demonstração do Ambiente

### 🐳 Gerenciamento de Infraestrutura (Docker)
Monitoramento dos containers via Docker Desktop, garantindo o controle de recursos como CPU e Memória.
<div align="center">
  <img src="Imagens1.png" width="850">
</div>

<br>

### ⚡ Interface de Testes (Swagger UI)
Documentação interativa da API para upload de PDFs e validação da `x-api-key`.
<div align="center">
  <img src="Imagens2.png" width="850">
</div>

<br>

### 🔍 Processamento e Logs
Visualização detalhada da extração de dados e logs de execução do servidor.
<div align="center">
  <img src="Imagens3.png" width="400">
  <img src="Imagens4.png" width="400">
  <img src="Imagens5.png" width="400">
</div>

---

## 📦 Como Instalar e Rodar

1. **Build da Imagem:**
   ```bash
   docker build -t juridiques-api .
   ```

2. **Execução do Container:**
   ```bash
   docker run -d -p 8000:8000 --name juridiques-container juridiques-api
   ```

---
Desenvolvido por [Liucera](https://github.com/Liucera)
