# Juridiques Zero ⚖️

Plataforma inteligente para simplificação de documentos jurídicos, evoluída de um script local para uma arquitetura robusta em nuvem. Este projeto é uma **Prova de Conceito (PoC)** de uma solução SaaS completa na AWS.

---

## 📈 Jornada de Desenvolvimento

### 🔹 Fase 1: O Protótipo (Backend)
Nascimento do projeto em Python puro para validação da lógica de extração de texto de PDFs jurídicos e limpeza de dados.

### 🔹 Fase 2: Modernização e Containerização (Docker)
Migração para Microserviços utilizando **Docker Compose**:
* **API:** FastAPI para alta performance.
* **Interface:** Streamlit para interação fluida.
* **Database:** PostgreSQL para persistência.
* **IA Local:** Orquestração do motor Phi-3 via Ollama.

### 🔹 Fase 3: Produção em Nuvem (AWS & IA)
Deploy real na **Amazon Web Services (AWS)** em instância **EC2**:
* **Infraestrutura:** Servidor Ubuntu com volumes EBS expandidos.
* **Cérebro:** Modelo **Phi-3** rodando localmente.
* **Rede:** Configuração de Security Groups e exposição de portas públicas.

---

## 🚀 Acesso ao Sistema
* **Interface:** [http://44.204.201.27:8501](http://44.204.201.27:8501)
* **API Swagger:** [http://44.204.201.27:8000/docs](http://44.204.201.27:8000/docs)
* **Redoc:** [http://44.204.201.27:8000/redoc](http://44.204.201.27:8000/redoc)

---

## 📸 Galeria de Implementação (13 Capturas)

| 🛡️ Painel AWS EC2 | 🖥️ Interface do Usuário | ⚙️ Swagger API |
| :---: | :---: | :---: |
| ![AWS](docs/aws_painel.PNG) | ![Interface](docs/interface.PNG) | ![Swagger](docs/swagger.PNG) |

| 📄 Redoc Profissional | ⚖️ Resultado IA | 🛠️ Log de Sistema |
| :---: | :---: | :---: |
| ![Redoc](docs/redoc.PNG) | ![Resultado](docs/tela_inicial.PNG) | ![Log](docs/log_execucao.PNG) |

---

## ⚠️ Análise de Viabilidade e Ressalvas
* **Gargalo de Hardware:** O processamento via CPU gera latência (média 4min). Para produção, é indispensável o uso de **GPUs**.
* **Consumo de Memória:** O modelo Phi-3 exige cerca de 4GB de RAM estável.
* **Escalabilidade:** Prevista hibridização com APIs externas (OpenAI/Groq) para ganho de performance.

---
*Desenvolvido por Arlindo da Silva Barroso - Especialista Cloud & Logística.*
