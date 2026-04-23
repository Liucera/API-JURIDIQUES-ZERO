# ⚖️ Juridiques Zero - Arquitetura Conteinerizada

Este projeto representa a evolução de uma ferramenta de extração de dados para uma arquitetura moderna de microserviços, focada em segurança, escalabilidade e provisionamento profissional.

---

## 🏗️ Arquitetura do Sistema (Explicação Técnica)

Abaixo, detalhamos a infraestrutura que compõe o ecossistema do projeto:

![Arquitetura do Sistema](./docs/imagem7.png)

### 1. Camada de Hospedagem (WSL2 + Docker Compose)
O projeto utiliza o **WSL2** para criar um ambiente Linux isolado dentro do Windows. O uso do **Docker Compose** garante que nada "polua" o sistema operacional principal. Isso significa que, se você levar este projeto para a **AWS** amanhã, ele rodará exatamente do mesmo jeito.

### 2. Orquestração de Microserviços
O sistema não é um bloco único, mas uma rede coordenada:
* **Contêiner API (O Cérebro):** Fica nos bastidores. É especialista em logística de dados: recebe o PDF, usa a biblioteca **PyMuPDF** para extrair o texto e devolve uma resposta estruturada (JSON).
* **Contêiner Interface (A Vitrine):** É a porta de entrada para o usuário. Gerencia o upload do documento e a interação visual via **Streamlit**.

### 3. Rede Interna (Service Discovery)
Um dos grandes marcos deste projeto foi a implementação do Service Discovery. Em vez de usar IPs locais (`127.0.0.1`), os contêineres se comunicam pelo nome do serviço (`http://api:8000`). Isso simula o funcionamento de grandes centros de dados.

### 4. Segurança e Configuração (.env)
Utilizamos o padrão ouro de segurança em Cloud: as chaves de API não estão escritas no código, mas são injetadas pelos contêineres através de arquivos `.env`. Isso evita exposições acidentais em repositórios públicos.

### 5. Sistema Híbrido
O processamento pesado do PDF ocorre localmente no Docker, enquanto a inteligência de tradução busca a nuvem da **OpenAI**, garantindo agilidade e precisão.

---

## 📸 Demonstração do Ambiente Operacional

Aqui vemos a integração em tempo real entre os serviços:

<p align="center">
  <img src="./docs/imagem6.png" width="45%" title="Interface Streamlit" />
  <img src="./docs/imagem8.png" width="45%" title="Monitoramento Docker Desktop" />
</p>

* **À esquerda:** A interface pronta para receber o documento jurídico.
* **À direita:** O monitoramento via Docker Desktop, garantindo o controle de recursos como CPU e Memória de cada contêiner.

---

## ⏳ Galeria de Evolução: O Processo Anterior

Antes da arquitetura final, o projeto passou por fases de validação fundamentais para garantir a precisão da extração:

<p align="center">
  <img src="./docs/imagem1.png" width="18%" />
  <img src="./docs/imagem2.png" width="18%" />
  <img src="./docs/imagem3.png" width="18%" />
  <img src="./docs/imagem4.png" width="18%" />
  <img src="./docs/imagem5.png" width="18%" />
</p>

### O que estas imagens representam:
1.  **Validação de Metadados:** Transição da leitura bruta para a extração inteligente de textos de processos.
2.  **Segurança de Header:** Implementação da `x-api-key` (Juridiques2026) para proteção dos endpoints.
3.  **Logs de Depuração:** Monitoramento constante da comunicação entre o motor de extração e o servidor Uvicorn.

---

## 🚀 Como Executar
1. `git clone https://github.com/Liucera/API-JURIDIQUES-ZERO.git`
2. Configure seu arquivo `.env` com sua chave da OpenAI.
3. Execute: `docker-compose up --build`
