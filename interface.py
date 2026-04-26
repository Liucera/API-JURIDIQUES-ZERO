import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Juridiques Zero", layout="wide")

st.title("⚖️ Juridiques Zero - Gestão Documental Inteligente")

# --- CRIAÇÃO DAS ABAS ---
tab1, tab2 = st.tabs(["🚀 Tradutor e Upload", "📂 Arquivo Digital (Banco de Dados)"])

with tab1:
    st.markdown("### 🤖 Tradução e Processamento Local")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✍️ Digite o texto jurídico")
        texto_input = st.text_area("Cole aqui...", height=200)

    with col2:
        st.markdown("### 📄 Ou suba um arquivo PDF")
        arquivo_pdf = st.file_uploader("Arraste seu PDF aqui", type=["pdf"])

    st.divider()

    if st.button("🚀 Traduzir Localmente (IA Local)"):
        with st.spinner('IA processando no servidor local...'):
            if arquivo_pdf:
                files = {"file": (arquivo_pdf.name, arquivo_pdf.getvalue())}
                headers = {"x-api-key": "Juridiques2026"}

                try:
                    # A API agora faz TUDO: lê, traduz com Ollama e salva no Banco
                    response = requests.post("http://api:8000/upload", files=files, headers=headers)

                    if response.status_code == 200:
                        resultado = response.json()
                        st.success("✅ Processado 100% Localmente!")
                        
                        st.markdown("### ✨ Resultado da IA Local:")
                        st.write(resultado.get("traducao"))
                    else:
                        st.error(f"Erro na API: {response.status_code}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")
            
            elif texto_input:
                st.warning("Para textos manuais, a integração direta será na próxima carga. Por enquanto, use PDFs!")

with tab2:
    st.header("📂 Documentos Imortalizados no Banco")

    # Nova barra de pesquisa
    termo_busca = st.text_input("🔍 Digite o nome do arquivo para buscar no arquivo digital:")

    if st.button("🔄 Consultar Banco"):
        try:
            # Passamos o termo de busca para a API
            params = {"busca": termo_busca} if termo_busca else {}
            response = requests.get("http://api:8000/documentos", params=params)

            if response.status_code == 200:
                dados = response.json()
                if dados:
                    df = pd.DataFrame(dados)
                    colunas_view = ["id", "nome_arquivo", "categoria", "data_processamento"]
                    st.dataframe(df[colunas_view], use_container_width=True)
                    st.info(f"Foram encontrados {len(dados)} documentos.")
                else:
                    st.warning("Nenhum documento encontrado com esse nome.")
            else:
                st.error("Erro ao buscar dados do banco.")
        except Exception as e:
            st.error(f"Não foi possível conectar à API: {e}")
