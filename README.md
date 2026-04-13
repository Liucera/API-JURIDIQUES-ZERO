# ⚖️ API Juridiques Zero

Uma solução inteligente para desmistificar o "juridiquês", automatizando a extração de dados críticos e a análise de documentos judiciais.

## 🚀 Sobre o Projeto
Esta API foi desenvolvida para transformar documentos jurídicos complexos em informações acionáveis. Utilizando a biblioteca **PyMuPDF**, ela processa PDFs nativos com alta velocidade, permitindo que advogados e analistas foquem no que importa.

### ✨ Funcionalidades
- **Extração Técnica:** Captura de texto puro e metadados.
- **Segurança:** Proteção por chave de acesso no Header.
- **Portabilidade:** Deploy simplificado via Docker.

---

## 📸 Demonstração e Prints

<div align="center">
  <h3>Interface Swagger e Testes</h3>
  <img src="Imagens1.png" width="800">
  <br><br>
  <h3>Processamento de Documentos</h3>
  <img src="Imagens2.png" width="400">
  <img src="Imagens3.png" width="400">
  <br><br>
  <h3>Logs e Validação</h3>
  <img src="Imagens4.png" width="400">
  <img src="Imagens5.png" width="400">
</div>

---

## 📦 Como Instalar
```bash
docker build -t juridiques-api .
docker run -d -p 8000:8000 --name juridiques-container juridiques-api
```

---
Desenvolvido por [Liucera](https://github.com/Liucera)
