import streamlit as st
from supabase import create_client
from datetime import datetime, timezone

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Painel de Administração")
st.title("🛡️ Painel de Controle")

# --- LOGIN ---
if "logado" not in st.session_state: st.session_state["logado"] = False

if not st.session_state["logado"]:
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar") and senha == "1234":
        st.session_state["logado"] = True
        st.rerun()
else:
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.rerun()

    # Buscar dados
    response = supabase.table("prestadores").select("*").execute()
    prestadores = response.data

    # Cabeçalho da tabela
    st.write("---")
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    c1.write("**Prestador**")
    c2.write("**Referência**")
    c3.write("**Pagamento**")
    c4.write("**Tempo**")

    for p in prestadores:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        col1.write(p['nome_prestador'])
        col2.write(p.get('referencia_pagamento', 'N/A'))
        
        status = p['status_pagamento']
        inicio_str = p.get('inicio_servico')
        
        # Lógica de Controle
        if status and inicio_str:
            inicio = datetime.fromisoformat(inicio_str.replace('Z', '+00:00'))
            agora = datetime.now(timezone.utc)
            decorrido = (agora - inicio).total_seconds()
            restante = 7200 - decorrido 

            if restante > 0:
                col3.write("✅ SIM")
                col4.write(f"⏳ {int(restante//60)}m")
            else:
                # Fechamento automático no banco
                supabase.table("prestadores").update({
                    "status_pagamento": False, 
                    "inicio_servico": None
                }).eq("id", p['id']).execute()
                st.rerun()
        else:
            col3.write("❌ NÃO")
            if col4.button("Pagar", key=f"btn_{p['id']}"):
                agora_iso = datetime.now(timezone.utc).isoformat()
                supabase.table("prestadores").update({
                    "status_pagamento": True, 
                    "inicio_servico": agora_iso
                }).eq("id", p['id']).execute()
                st.rerun()
