import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta, timezone

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Painel de Administração")
st.title("🛡️ Painel de Controle")

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

    response = supabase.table("prestadores").select("*").execute()
    prestadores = response.data

    for p in prestadores:
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write(f"**{p['nome_prestador']}**")
        
        status = p['status_pagamento']
        inicio_str = p.get('inicio_servico')
        
        # Lógica do Cronômetro
        if status and inicio_str:
            inicio = datetime.fromisoformat(inicio_str.replace('Z', '+00:00'))
            agora = datetime.now(timezone.utc)
            decorrido = (agora - inicio).total_seconds()
            restante = 7200 - decorrido # 7200 segundos = 2h

            if restante > 0:
                col2.write(f"⏳ {int(restante//60)}m {int(restante%60)}s")
                col3.button("Pagar", key=f"d_{p['id']}", disabled=True)
            else:
                # Tempo esgotado: fecha automaticamente
                supabase.table("prestadores").update({"status_pagamento": False, "inicio_servico": None}).eq("id", p['id']).execute()
                st.rerun()
        else:
            col2.write("---")
            if col3.button("Pagar", key=f"a_{p['id']}"):
                # Inicia o tempo agora
                agora_iso = datetime.now(timezone.utc).isoformat()
                supabase.table("prestadores").update({"status_pagamento": True, "inicio_servico": agora_iso}).eq("id", p['id']).execute()
                st.rerun()
