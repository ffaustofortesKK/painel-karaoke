import streamlit as st
from supabase import create_client

# --- CONFIGURAÇÃO ---
# No Streamlit Cloud, em Settings -> Secrets, você deve ter:
# URL_SUPABASE = "https://woblqkukbooyezvwtukb.supabase.co"
# KEY_SUPABASE = "SUA_CHAVE_ANON_AQUI"

try:
    # Acessa os nomes definidos no painel Secrets do Streamlit
    url = st.secrets["URL_SUPABASE"]
    key = st.secrets["KEY_SUPABASE"]
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Erro ao carregar configurações: {e}")
    st.stop()

st.set_page_config(page_title="Painel de Administração")
st.title("🛡️ Painel de Controle")

# --- LOGIN ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    senha = st.text_input("Digite a senha de administrador:", type="password")
    if st.button("Entrar"):
        if senha == "1234":
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
else:
    # --- PAINEL PRINCIPAL ---
    st.write("Conectado ao Banco de Dados.")
    
    # Buscar prestadores
    try:
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
    except Exception as e:
        st.error(f"Erro ao buscar ou atualizar dados: {e}")
    
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.rerun()
