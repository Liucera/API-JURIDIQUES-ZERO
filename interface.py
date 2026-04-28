import streamlit as st
import requests
import pandas as pd

"""
Interface do Usuário - Juridiques Zero.
Construída com Streamlit, esta aplicação oferece uma interface visual para upload de PDFs,
visualização de traduções geradas por IA e consulta ao histórico no banco de dados.
"""

# Configurações globais da página
st.set_page_config(page_title="Juridiques Zero", layout="wide", page_icon="⚖️")

st.title("⚖️ Juridiques Zero - Gestão Documental Inteligente")

# Organização da interface em abas para melhor UX
tab1, tab2 = st.tabs(["🚀 Tradutor e Upload", "📂 Arquivo Digital (Banco de Dados)"])

with tab1:
    st.markdown("### 🤖 Tradução e Processamento Local")
    st.info("O processamento é feito 100% localmente para garantir a privacidade dos dados.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✍️ Digite o texto jurídico")
        texto_input = st.text_area("Cole aqui termos ou parágrafos para tradução...", height=200)

    with col2:
        st.markdown("### 📄 Ou suba um arquivo PDF")
        arquivo_pdf = st.file_uploader("Arraste seu PDF aqui (Contratos, Petições, etc.)", type=["pdf"])

    st.divider()

    # Gatilho para iniciar o processamento
    if st.button("🚀 Traduzir Localmente (IA Local)"):
        with st.spinner('IA processando no servidor local... Este processo pode levar alguns minutos em CPUs comuns.'):
            if arquivo_pdf:
                # Prepara o arquivo para o envio via POST
                files = {"file": (arquivo_pdf.name, arquivo_pdf.getvalue())}
                headers = {"x-api-key": "Juridiques2026"}

                try:
                    # Envia para a API Backend (FastAPI)
                    # O container 'api' é resolvido internamente pela rede do Docker
                    response = requests.post("http://api:8000/upload", files=files, headers=headers)

                    if response.status_code == 200:
                        resultado = response.json()
                        st.success("✅ Processado com sucesso!")
                        
                        st.markdown("### ✨ Resultado da Simplificação:")
                        st.write(resultado.get("traducao"))

                        with st.expander("Ver texto original extraído"):
                            st.text(resultado.get("content"))
                    else:
                        st.error(f"Erro na API: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Erro de conexão com o backend: {e}")
            
            elif texto_input:
                st.warning("A tradução direta de texto manual está em desenvolvimento. Por favor, utilize o upload de PDF para esta versão.")

with tab2:
    st.header("📂 Documentos Imortalizados no Banco")
    st.markdown("Consulte aqui o histórico de arquivos processados e salvos no PostgreSQL.")

    # Ferramenta de busca por nome de arquivo
    termo_busca = st.text_input("🔍 Buscar por nome do arquivo:")

    if st.button("🔄 Consultar Banco de Dados"):
        try:
            # Solicita a lista de documentos para a API
            params = {"busca": termo_busca} if termo_busca else {}
            response = requests.get("http://api:8000/documentos", params=params)

            if response.status_code == 200:
                dados = response.json()
                if dados:
                    # Converte a lista JSON em um DataFrame do Pandas para exibição em tabela
                    df = pd.DataFrame(dados)
                    # Seleciona apenas as colunas relevantes para o usuário
                    colunas_view = ["id", "nome_arquivo", "categoria", "data_processamento"]
                    st.dataframe(df[colunas_view], use_container_width=True)
                    st.info(f"Foram encontrados {len(dados)} registro(s).")
                else:
                    st.warning("Nenhum documento encontrado para o termo pesquisado.")
            else:
                st.error("Erro ao recuperar dados do banco.")
        except Exception as e:
            st.error(f"Não foi possível conectar à API: {e}")
