import streamlit as st
import requests

st.set_page_config(page_title="Painel de Administração", layout="wide")
st.title("🛡️ Painel de Controle")

# URL BASE do Firebase
BASE_URL = "https://grupoffkaraoke-default-rtdb.firebaseio.com"

# --- LOGIN ---
if "logado" not in st.session_state: st.session_state["logado"] = False
if not st.session_state["logado"]:
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar") and senha == "1234":
        st.session_state["logado"] = True
        st.rerun()
    st.stop()

# --- SEÇÃO: FILA DE PRESTADORES ---
st.subheader("🎤 Fila de Prestadores")

if st.button("🔄 Atualizar Fila"):
    st.rerun()

try:
    # Busca os prestadores diretamente no Firebase
    response = requests.get(f"{BASE_URL}/prestadores.json")
    prestadores_data = response.json()
    
    if prestadores_data:
        # Cabeçalhos
        header1, header2, header3 = st.columns([3, 2, 1])
        header1.write("**Prestador**")
        header2.write("**Telefone (ID)**")
        header3.write("**Ação**")

        # Loop pelos prestadores do Firebase
        # 'prestadores_data' vem como um dicionário {telefone: dados_do_prestador}
        for tel, dados in prestadores_data.items():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            nome_display = dados.get('nome', 'Sem Nome')
            
            col1.write(f"👤 {nome_display}")
            col2.write(f"📞 {tel}")
            
            # Botão de Remover prestador (exemplo de ação)
            if col3.button("🗑️", key=f"del_{tel}"):
                requests.delete(f"{BASE_URL}/prestadores/{tel}.json")
                st.rerun()
    else:
        st.info("Nenhum prestador registado no Firebase.")
        
except Exception as e:
    st.error(f"Erro ao conectar ao Firebase: {e}")
