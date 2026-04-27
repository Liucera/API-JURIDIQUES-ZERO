# Juridiques Zero ⚖️

Plataforma inteligente para simplificação de documentos jurídicos. Este projeto é uma **Prova de Conceito (PoC)** de uma solução SaaS completa, integrando infraestrutura de nuvem, IA local e APIs modernas.

---

## 📈 Jornada Técnica de Desenvolvimento

### 🔹 Fase 1: O Protótipo (Backend)
Desenvolvimento da lógica principal em Python para extração de texto de PDFs jurídicos complexos e estruturação de dados para processamento.

### 🔹 Fase 2: Containerização (Docker)
Migração para arquitetura de microserviços utilizando **Docker Compose**, garantindo isolamento entre a API (FastAPI), a interface (Streamlit) e o motor de IA.

### 🔹 Fase 3: Deploy Cloud (AWS EC2)
Implementação em ambiente de produção real na **Amazon Web Services (AWS)**:
* Instância **m7i-flex.large** no Ubuntu.
* Configuração de Security Groups, portas de rede e volumes EBS.
* Orquestração do modelo **Phi-3** para processamento local.

---

## 🚀 Acesso e Demonstração
* **Interface Streamlit:** [http://44.204.201.27:8501](http://44.204.201.27:8501)
* **Documentação Swagger:** [http://44.204.201.27:8000/docs](http://44.204.201.27:8000/docs)
* **Documentação Redoc:** [http://44.204.201.27:8000/redoc](http://44.204.201.27:8000/redoc)

---

## 📸 Galeria de Implementação e Evidências

| 🛡️ Painel AWS EC2 | 🖥️ Interface do Usuário | ⚙️ Swagger API |
| :---: | :---: | :---: |
| ![AWS](docs/aws_painel.PNG) | ![Interface](docs/interface.PNG) | ![Swagger](docs/swagger.PNG) |

| 📄 Redoc Profissional | ⚖️ Resultado IA | 🛠️ Log de Sistema |
| :---: | :---: | :---: |
| ![Redoc](docs/redoc.PNG) | ![Resultado](docs/tela_inicial.PNG) | ![Log](docs/log_execucao.PNG) |

---

## ⚠️ Ressalvas Técnicas e Próximos Passos
* **Hardware:** Processamento via CPU apresenta latência. Recomendado o uso de **GPU** para produção.
* **Recursos:** Consumo estável de 4GB RAM para o modelo local.
* **Escalabilidade:** Estrutura preparada para transição para APIs de alta performance (Groq/OpenAI).

---
*Desenvolvido por Arlindo da Silva Barroso - Especialista Cloud & Logística.*
