import streamlit as st
from supabase import create_client

# --- CONFIGURAÇÃO ---
# No Streamlit Cloud, vá em Settings -> Secrets e coloque:
# URL_SUPABASE = "sua_url_aqui"
# KEY_SUPABASE = "sua_chave_aqui"

try:
    url = st.secrets["URL_SUPABASE"]
    key = st.secrets["KEY_SUPABASE"]
    supabase = create_client(url, key)
except:
    st.error("Configurações de segredos (secrets) não encontradas no Streamlit.")

st.set_page_config(page_title="Painel de Administração")
st.title("🛡️ Painel de Controle")

# --- LOGIN ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    senha = st.text_input("Digite a senha de administrador:", type="password")
    if st.button("Entrar"):
        if senha == "1234": # Mude a senha aqui
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
else:
    # --- PAINEL PRINCIPAL ---
    st.write("Conectado ao Banco de Dados.")
    
    # Buscar prestadores
    response = supabase.table("prestadores").select("*").execute()
    prestadores = response.data
    
    if not prestadores:
        st.write("Nenhum prestador cadastrado.")
    else:
        for p in prestadores:
            col1, col2 = st.columns([3, 1])
            col1.write(f"**Prestador:** {p['nome_prestador']} | **Ref:** {p['referencia_pagamento']}")
            
            # Botão de status
            status = p['status_pagamento']
            if col2.button("Sim" if status else "Não", key=str(p['id'])):
                novo_status = not status
                supabase.table("prestadores").update({"status_pagamento": novo_status}).eq("id", p['id']).execute()
                st.rerun()
    
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.rerun()
