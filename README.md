# ⚖️ Juridiques Zero API (PROVA DE CONCEITO)
> **Transformando o "Juridiquês" em clareza através de IA e Cloud Computing.**

---
## 🏗️ Arquitetura Visual

´´´mermaid

graph TD
    User((👤 Usuário)) -->|Upload PDF| Streamlit[🖥️ Interface: Streamlit]
    subgraph Docker_Network [Rede Interna Docker]
        Streamlit -->|POST /upload| FastAPI[⚙️ API: FastAPI]
        
        subgraph IA_Engine [Processamento Local]
            FastAPI -->|Extração| PyPDF2[📄 PyPDF2]
            FastAPI -->|Prompt| Ollama[🧠 Ollama: phi-3]
            Ollama -->|Tradução| FastAPI
        end
        
        subgraph Database [Dados]
            FastAPI -->|Salva| Postgres[(🐘 PostgreSQL)]
        end
    end

    FastAPI -->|Resposta| Streamlit
    Streamlit -->|Resultado| User

    style Streamlit fill:#f9f,stroke:#333

## 🚀 O que é o Projeto?
O **Juridiques Zero** é uma solução Full Stack projetada para resolver o abismo de comunicação entre advogados e clientes. Muitas vezes, o cliente recebe uma atualização processual ou um contrato e não compreende o impacto real daquelas palavras técnicos.

**Nosso Diferencial:** Utilizamos Inteligência Artificial local (Ollama/Phi-3) para processar documentos e extrair o "sumário executivo" em linguagem simples, integrando automação de banco de dados e uma interface intuitiva.

---

## 🛠️ Problema Jurídico que Resolve
O projeto foca na **Gestão de Transparência Processual**. 
* **Foco:** Gestão de Processos e Contratos.
* **Solução:** Redução de chamados e dúvidas de clientes ao fornecer uma tradução automática de termos técnicos para linguagem leiga, centralizando cadastros de clientes e processos de forma organizada.

---

## 📷 Evidências do Sistema
Abaixo, as capturas de tela que comprovam a infraestrutura rodando na AWS:

### Interface do Usuário (Streamlit)
![Interface Principal](docs/interface1.png)

### Painel de Controle AWS
![Painel AWS](docs/aws_painel1.png)

### Documentação Técnica (Swagger & ReDoc)
![Swagger](docs/swagger1.png)
![ReDoc](docs/redoc1.png)

---

## 🛣️ Guia de Instalação (Passo a Passo)

### Pré-requisitos
* Docker & Docker Compose instalados.
* Instância EC2 (recomendado t3.medium ou superior para rodar a IA local).

### Como Rodar
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Liucera/api-juridiques-zero.git](https://github.com/Liucera/api-juridiques-zero.git)
    cd api-juridiques-zero
    ```

2.  **Suba os containers:**
    ```bash
    docker-compose up -d
    ```

3.  **Acesse o sistema:**
    * **Interface Web:** `http://seu-ip:8501`
    * **Documentação API:** `http://seu-ip:8000/docs`

---

## 🔌 Endpoints da API (Swagger)
A API foi construída com FastAPI, garantindo performance e documentação automática.

* `GET /health`: Verifica se o motor de IA e o banco estão online.
* `POST /processos`: Cadastro de novos processos judiciais.
* `POST /clientes`: Gestão de base de dados de clientes.
* `POST /traduzir`: O ponto alto do projeto. Envie um texto jurídico e receba a versão simplificada.

---

## 💡 Exemplos Reais de Uso
1.  **Cadastro de Processo:** O advogado insere o número `0001234-56.2024.8.06.0001` e o status "Concluso para despacho".
2.  **Tradução de Termo:** Ao inserir "Concluso para despacho", a IA retorna: *"O seu processo está na mesa do juiz aguardando uma decisão simples."*
3.  **Gestão de Contratos:** Armazenamento de PDFs de contratos para consulta rápida.

---

## 🏗️ Arquitetura Técnica
* **Backend:** FastAPI (Python)
* **Frontend:** Streamlit
* **IA:** Ollama (Phi-3)
* **Banco de Dados:** PostgreSQL
* **Infra:** AWS (EC2 & Docker)

## ⚠️ Análise Técnica e Ressalvas (Performance & Escalabilidade)

Como este projeto é uma Prova de Conceito, foram identificados pontos cruciais para a viabilidade de uma versão comercial:

* **Gargalo de Latência:** O processamento atual (média de 4 minutos) ocorre via CPU. Em um ambiente de produção, é necessária a migração para **instâncias com GPU (AWS família G)** para reduzir a resposta para segundos.
* **Otimização de Recursos:** A execução de LLMs locais consome elevada memória RAM (aprox. 4GB para o Phi-3). Recomenda-se o uso de **Cache (Redis/Postgres)** para evitar reprocessamento de documentos idênticos.
* **Estratégia Híbrida:** Para maior agilidade e menor custo fixo de hardware, o projeto prevê a possibilidade de conexão com **APIs externas (Groq/OpenAI)**, garantindo desempenho instantâneo.
* **Objetivo:** Este projeto demonstra a capacidade técnica de orquestrar um fluxo SaaS completo, desde a codificação até a gestão de instâncias em nuvem.

Desenvolvido por Arlindo Barroso -- Aluno do CAPACITA-IREDE
