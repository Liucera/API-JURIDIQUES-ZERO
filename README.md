# ⚖️ API Juridiques Zero

Uma solução inteligente para desmistificar o "juridiquês", automatizando a extração de dados críticos e a análise de documentos judiciais.

## 🚀 Sobre o Projeto
Esta API foi desenvolvida para transformar documentos jurídicos complexos em informações acionáveis. Utilizando uma arquitetura moderna, ela serve como base para processamento de linguagem natural (NLP) e extração de metadados, identificando conteúdos essenciais em arquivos PDF.

### ✨ Funcionalidades Atuais
- **Extração de Texto:** Leitura técnica e de alta performance de arquivos PDF via PyMuPDF.
- **Segurança Nativa:** Proteção via cabeçalho `x-api-key`, garantindo que apenas usuários autorizados acessem o serviço.
- **Arquitetura Robusta:** Totalmente conteinerizada com Docker, pronta para deploy escalável.
- **Documentação Automática:** Interface interativa via Swagger UI.

## 🛠️ Tecnologias Utilizadas
- **Python 3.11+** 🐍
- **FastAPI:** Framework moderno e de alta performance.
- **PyMuPDF (fitz):** Biblioteca líder em precisão para extração de PDFs.
- **Docker:** Padronização do ambiente de execução.

## 📦 Como Instalar e Rodar

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Liucera/API-JURIDIQUES-ZERO.git
   cd API-JURIDIQUES-ZERO
   ```

2. **Construa a imagem Docker:**
   ```bash
   docker build -t juridiques-api .
   ```

3. **Inicie o container:**
   ```bash
   docker run -d -p 8000:8000 --name juridiques-container juridiques-api
   ```

## 🔐 Segurança e Autenticação

Para utilizar os endpoints da API, inclua a chave no cabeçalho:
- **Header:** `x-api-key`
- **Chave padrão:** `Juridiques2026`

---
Desenvolvido por [Liucera](https://github.com/Liucera)
