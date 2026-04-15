import streamlit as st
import requests
from openai import OpenAI

# 1. Configuração da OpenAI
# Substitua pela sua chave real se esta não funcionar
client = OpenAI(api_key="COLOQUE_SUA_CHAVE_AQUI")

st.set_page_config(page_title="Juridiquês Zero", layout="wide", page_icon="⚖️")

st.title("⚖️ Juridiquês Zero")
st.subheader("Transforme termos complexos em linguagem clara e acessível.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Digite o texto jurídico")
    texto_input = st.text_area("Cole o parágrafo do processo aqui...", height=300)

with col2:
    st.markdown("### 📄 Ou suba um arquivo PDF")
    arquivo_pdf = st.file_uploader("Arraste seu PDF aqui", type=["pdf"])

st.divider()

if st.button("🚀 Traduzir para Linguagem Simples"):
    texto_para_traduzir = ""

    with st.spinner('Processando informações...'):
        # LÓGICA PARA PDF (Chama sua API no Terminal 1)
        if arquivo_pdf:
            files = {"file": arquivo_pdf}
            # A chave abaixo deve ser a mesma que você colocou no app/main.py
            headers = {"x-api-key": "Juridiques2026"} 
            
            try:
                # Usando o IP 127.0.0.1 que é o mais estável para o seu computador
                response = requests.post("http://127.0.0.1:8000/upload", files=files, headers=headers)
                
                if response.status_code == 200:
                    texto_para_traduzir = response.json().get("content", "")
                else:
                    st.error(f"Erro na API: Status {response.status_code}")
            except Exception as e:
                st.error(f"Não foi possível conectar na API. Verifique se o Terminal 1 está rodando! Erro: {e}")

        # LÓGICA PARA TEXTO DIRETO
        elif texto_input:
            texto_para_traduzir = texto_input

        # CHAMADA PARA OPENAI
        if texto_para_traduzir:
            prompt = f"Traduza o seguinte texto jurídico para uma linguagem extremamente simples e fácil de entender por qualquer pessoa, mantendo os fatos principais:\n\n{texto_para_traduzir}"
            
            try:
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Você é um tradutor especialista em direito para leigos."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                traducao = completion.choices[0].message.content
                
                st.success("Tradução Concluída!")
                
                with st.expander("🔍 Ver texto original processado"):
                    st.text(texto_para_traduzir)
                
                st.markdown("### ✨ Resultado:")
                st.write(traducao)
            except Exception as e:
                st.error(f"Erro na OpenAI: {e}")
        else:
            st.warning("Por favor, digite um texto ou suba um PDF.")
