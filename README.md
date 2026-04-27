# Juridiques Zero ⚖️

Uma plataforma inteligente para simplificação de documentos jurídicos, desenvolvida como uma **Prova de Conceito (PoC)** de uma solução SaaS completa, abrangendo desde o backend local até o deploy em infraestrutura de nuvem escalável.

---

## 📈 Jornada de Evolução e Infraestrutura

Este repositório documenta a progressão técnica do projeto:

1.  **Fase 1: Backend Funcional** – Extração de dados de PDFs utilizando Python e FastAPI.
2.  **Fase 2: Arquitetura de Microserviços** – Containerização com Docker e Docker Compose, separando API, Interface (Streamlit) e Banco de Dados (PostgreSQL).
3.  **Fase 3: Deploy em Nuvem (AWS EC2)** – Execução em instância `m7i-flex.large` na Amazon Web Services, com orquestração de IA local via Ollama.

---

## 📸 Demonstração e Documentação

### 🌐 Links de Acesso Direto
* **Interface Streamlit:** [http://44.204.201.27:8501](http://44.204.201.27:8501)
* **API Swagger:** [http://44.204.201.27:8000/docs](http://44.204.201.27:8000/docs)
* **Redoc:** [http://44.204.201.27:8000/redoc](http://44.204.201.27:8000/redoc)

### 🖼️ Screenshots do Sistema
| Interface Streamlit | Painel AWS EC2 | Documentação API (Swagger) |
| :--- | :--- | :--- |
| ![Interface](./docs/screenshots/interface_streamlit_sucesso.png) | ![AWS](./docs/screenshots/aws_ec2_painel.png) | ![Swagger](./docs/screenshots/swagger_api_docs.png) |

---

## ⚠️ Análise Técnica e Ressalvas (Performance & Escalabilidade)

Como este projeto é uma Prova de Conceito, foram identificados pontos cruciais para a viabilidade de uma versão comercial:

* **Gargalo de Latência:** O processamento atual (média de 4 minutos) ocorre via CPU. Em um ambiente de produção, é necessária a migração para **instâncias com GPU (AWS família G)** para reduzir a resposta para segundos.
* **Otimização de Recursos:** A execução de LLMs locais consome elevada memória RAM (aprox. 4GB para o Phi-3). Recomenda-se o uso de **Cache (Redis/Postgres)** para evitar reprocessamento de documentos idênticos.
* **Estratégia Híbrida:** Para maior agilidade e menor custo fixo de hardware, o projeto prevê a possibilidade de conexão com **APIs externas (Groq/OpenAI)**, garantindo desempenho instantâneo.
* **Objetivo:** Este projeto demonstra a capacidade técnica de orquestrar um fluxo SaaS completo, desde a codificação até a gestão de instâncias em nuvem.

---
*Desenvolvido por Arlindo da Silva Barroso - Especialista em Logística e Desenvolvedor focado em Cloud Computing.*

## 📈 Jornada de Evolução
Este repositório documenta a evolução completa de uma solução de engenharia de software:

* **Fase 1 (Local):** Construção de um backend funcional em Python/FastAPI para extração de PDFs.
* **Fase 2 (Containerização):** Migração para arquitetura de microserviços utilizando **Docker** e **Docker Compose**, separando as camadas de lógica (API) e apresentação (Interface).
* **Fase 3 (IA & Cloud - ATUAL):** * Deploy em produção na **AWS (Amazon EC2)**.
    * Integração do LLM **Phi-3** rodando localmente no servidor via Ollama.
    * Banco de dados PostgreSQL containerizado para persistência.

---
*(Abaixo segue a documentação detalhada de cada módulo)*

---

## 🏗️ Arquitetura do Sistema (Provisionamento PSC)

Abaixo, detalhamos a infraestrutura conteinerizada que compõe o ecossistema:

### 1. Orquestração de Microserviços
O sistema utiliza **Docker Compose** para gerenciar quatro serviços integrados:
* **API (FastAPI):** O cérebro logístico. Extrai texto de PDFs via `PyPDF2` e coordena a IA e o banco de dados.
* **IA Local (Ollama/Llama 3):** Processamento de linguagem natural rodando localmente, eliminando custos com APIs externas.
* **Banco de Dados (PostgreSQL):** "Arquivo Digital" persistente que imortaliza cada documento processado.
* **Interface (Streamlit):** Porta de entrada visual para upload e consulta de documentos.

### 2. Rede Interna e Service Discovery
Os contêineres comunicam-se via nomes de serviço (`http://api:8000`), simulando um ambiente real de Data Center, sem exposição desnecessária de portas para o host.

---

## 🔌 Documentação da API (Swagger)
O projeto conta com documentação interativa automática para testes de endpoints.
👉 **Acesse em:** `http://localhost:8000/docs`

---

## 🚀 Como Executar (Passo a Passo)

1. **Clonar o Repositório:**
   ```bash
   git clone [https://github.com/Liucera/API-JURIDIQUES-ZERO.git](https://github.com/Liucera/API-JURIDIQUES-ZERO.git)
   cd API-JURIDIQUES-ZERO

2. Provisionar a Infraestrutura:

Bash
docker-compose up -d --build

3.0 Instalar o Modelo de IA (Obrigatório na primeira execução):

Bash
docker exec -it juridiques-ollama ollama run llama3

4.0 Acessar o Sistema:

Interface: http://localhost:8501

API Docs: http://localhost:8000/docs

5.0 📸 Demonstração do Ambiente Operacional
O monitoramento via Docker Desktop garante o controle de recursos (CPU/Memória) de cada serviço em tempo real.

---

## ⏳ Galeria de Evolução: O Processo de Desenvolvimento

Antes da arquitetura final com IA Local, o projeto passou por fases de validação fundamentais para garantir a precisão da extração e segurança:

<p align="center">
  <img src="./docs/imagem1.png" width="18%" />
  <img src="./docs/imagem2.png" width="18%" />
  <img src="./docs/imagem3.png" width="18%" />
  <img src="./docs/imagem4.png" width="18%" />
  <img src="./docs/imagem5.png" width="18%" />
</p>

### O que estas imagens representam:
* **Validação de Metadados:** Transição da leitura bruta para a extração inteligente.
* **Segurança de Header:** Implementação da chave de segurança `Juridiques2026`.
* **Logs de Depuração:** Monitorização da comunicação entre os microserviços.
## 📊 Fluxo de Arquitetura

```mermaid
graph TD
    User((👤 Usuário)) -->|Upload PDF| Streamlit[🖥️ Interface: Streamlit]
    
    subgraph Docker_Network [Rede Interna Docker]
        Streamlit -->|POST /upload| FastAPI[⚙️ API: FastAPI]
        
        subgraph IA_Engine [Processamento Local]
            FastAPI -->|Extração| PyPDF2[📄 PyPDF2]
            FastAPI -->|Prompt| Ollama[🧠 Ollama: Phi-3]
            Ollama -->|Tradução| FastAPI
        end
        
        subgraph Database [Dados]
            FastAPI -->|Salva| Postgres[(🐘 PostgreSQL)]
        end
    end

    FastAPI -->|Resposta| Streamlit
    Streamlit -->|Resultado| User

    style Streamlit fill:#f9f,stroke:#333
    style FastAPI fill:#00ffcc,stroke:#333
    style Ollama fill:#ff9900,stroke:#333
    style Postgres fill:#336791,stroke:#fff
```
