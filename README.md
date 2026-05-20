# Juridiques Zero

Simplificacao de documentos juridicos com Inteligencia Artificial local e hibrida.

## Versao

2.1.0 - IA Hibrida com React e Ollama local

## Arquitetura

- Frontend: React + Vite
- Backend: FastAPI (Python)
- IA Local: Ollama (gemma2:2b)
- IA Externa: Gemini (opcional)
- Cache: Redis
- Banco de Dados: PostgreSQL
- Infraestrutura: Docker Compose

## Requisitos

- Docker 24.0+
- Docker Compose 2.20+
- 12GB RAM (minimo recomendado)
- 20GB espaco em disco

## Deploy Local

```bash
# Clonar repositorio
git clone https://github.com/Liucera/API-JURIDIQUES-ZERO.git
cd API-JURIDIQUES-ZERO

# Subir stack
docker-compose up --build -d

# Aguardar Ollama baixar modelo (5-10 minutos primeiro deploy)
docker-compose logs -f ollama

| Servico         | URL                          |
| --------------- | ---------------------------- |
| Interface React | <http://localhost:5173>      |
| API FastAPI     | <http://localhost:8000>      |
| Swagger UI      | <http://localhost:8000/docs> |



Funcionalidades
Prompt Direto
Digite texto juridico para simplificacao instantanea.
Upload PDF
Arraste ou selecione documentos PDF para extracao e analise.
Modo Gemini (opcional)
Ative no toggle para processamento via API Google (mais rapido, custo variavel).
Cache Inteligente
Documentos ja processados retornam em menos de 1 segundo via Redis.
Estrutura de Precos

| Plano        | IA           | Tempo  | Custo            |
| ------------ | ------------ | ------ | ---------------- |
| Gratuito     | Ollama local | 30-40s | R\$ 0,00         |
| Profissional | Gemini       | 5-10s  | Variavel por uso |



GEMINI_API_KEY=sua_chave_aqui
docker-compose restart api


| Metodo | Endpoint     | Descricao              |
| ------ | ------------ | ---------------------- |
| GET    | /health      | Status do sistema      |
| POST   | /simplificar | Simplificar texto      |
| POST   | /upload      | Upload e processar PDF |
| GET    | /documentos  | Listar documentos      |
| GET    | /metricas    | Metricas de uso        |



| Variavel         | Padrao                                                      | Descricao     |
| ---------------- | ----------------------------------------------------------- | ------------- |
| DATABASE\_URL    | postgresql://admin:Juridiques2026\@db:5432/juridiques\_zero | PostgreSQL    |
| REDIS\_URL       | redis\://redis:6379/0                                       | Redis         |
| OLLAMA\_URL      | <http://ollama:11434>                                       | Ollama        |
| GEMINI\_API\_KEY | vazio                                                       | Google Gemini |



| Camada     | Tecnologia               |
| ---------- | ------------------------ |
| Frontend   | React 18, Vite, Axios    |
| Backend    | FastAPI, Uvicorn         |
| IA Local   | Ollama, gemma2:2b        |
| IA Externa | Google Gemini 2.0 Flash  |
| Cache      | Redis 7                  |
| Banco      | PostgreSQL 15 + pgvector |
| PDF        | PyPDF2                   |
| Deploy     | Docker Compose           |



| Metrica                      | Valor          |
| ---------------------------- | -------------- |
| Tempo primeiro processamento | 30-40 segundos |
| Tempo com cache              | < 1 segundo    |
| Taxa de cache hit            | ~60%           |
| Custo IA (modo local)        | R\$ 0,00       |



Roadmap
[x] IA local com Ollama
[x] Cache Redis
[x] Interface React
[x] Suporte Gemini
[ ] Autenticacao JWT
[ ] Multi-tenancy
[ ] RAG juridico brasileiro
[ ] White-label
[ ] Deploy AWS/GCP multi-cloud


Desenvolvedor
Arlindo Barroso
Aluno CAPACITA-IREDE
Licenca
MIT
