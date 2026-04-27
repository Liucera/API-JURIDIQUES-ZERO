# Juridiques Zero ⚖️

Uma plataforma inteligente para simplificação de documentos jurídicos, evoluída de um script local para uma arquitetura robusta em nuvem. Este projeto é uma **Prova de Conceito (PoC)** de uma solução SaaS completa na AWS.

---

## 📈 Jornada de Desenvolvimento

### 🔹 Fase 1: O Protótipo (Backend)
Nascimento do projeto em Python puro para validação da lógica de extração de texto de PDFs jurídicos e limpeza de dados.

### 🔹 Fase 2: Modernização e Containerização (Docker)
Migração para Microserviços utilizando **Docker Compose**:
* **API:** FastAPI para alta performance.
* **Interface:** Streamlit para interação fluida.
* **Database:** PostgreSQL para persistência.
* **IA Local:** Orquestração do Ollama.

### 🔹 Fase 3: Produção em Nuvem (AWS & IA)
Deploy real na **Amazon Web Services (AWS)** em instância **EC2**:
* **Infraestrutura:** Servidor Ubuntu com volumes EBS expandidos.
* **Cérebro:** Modelo **Phi-3** rodando localmente.
* **Rede:** Configuração de Security Groups e exposição de portas públicas.

---

## 🚀 Acesso e Testes
* **Interface:** [http://44.204.201.27:8501](http://44.204.201.27:8501)
* **Documentação Swagger:** [http://44.204.201.27:8000/docs](http://44.204.201.27:8000/docs)
* **Redoc:** [http://44.204.201.27:8000/redoc](http://44.204.201.27:8000/redoc)

---

## 📸 Galeria de Comprovação Técnica (13 Capturas)

| 🛡️ Infraestrutura AWS | 🖥️ Interface Sucesso | ⚙️ Swagger API |
| :---: | :---: | :---: |
| ![AWS](docs/aws_painel.png) | ![Interface](docs/interface.png) | ![Swagger](docs/swagger.png) |

| 📄 Redoc Profissional | ⚖️ Resultado IA | 🛠️ Erro Resolvido |
| :---: | :---: | :---: |
| ![Redoc](docs/redoc.png) | ![Resultado](docs/tela_inicial.png) | ![Erro](docs/erro_inicial.png) |

| 📊 Log de Rede | 📈 Monitoramento | 📂 Estrutura Docs |
| :---: | :---: | :---: |
| ![Log](docs/imagem1.png) | ![Monit](docs/imagem2.png) | ![Estrutura](docs/imagem3.png) |

| 🔄 Fluxo de Dados | 🔋 Consumo RAM | 📝 Documentação | 🏁 Conclusão |
| :---: | :---: | :---: | :---: |
| ![F1](docs/imagem4.png) | ![F2](docs/imagem5.png) | ![F3](docs/imagem6.png) | ![F4](docs/imagem7.png) |

---

## ⚠️ Análise de Viabilidade e Ressalvas
* **Gargalo de Hardware:** O processamento via CPU gera latência (média 4min). Para produção, é indispensável o uso de **GPUs**.
* **Consumo de Memória:** O modelo Phi-3 exige cerca de 4GB de RAM estável.
* **Estratégia de Cache:** Necessidade de implementar Cache (Redis/Postgres) para evitar reprocessamento desnecessário.
* **IA Híbrida:** O projeto prevê integração com APIs externas (Groq/OpenAI) para ganho de performance instantânea.

---
*Desenvolvido por Arlindo da Silva Barroso - Especialista Cloud & Logística.*
