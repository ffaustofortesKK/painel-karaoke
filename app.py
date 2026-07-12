import streamlit as st
from supabase import create_client
from datetime import datetime, timezone
from streamlit_autorefresh import st_autorefresh

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

# Atualiza a página automaticamente a cada 1000ms (1 segundo)
st_autorefresh(interval=1000, key="datarefresh")

st.set_page_config(page_title="Painel de Administração", layout="wide")
st.title("🛡️ Painel de Controle em Tempo Real")

# --- LOGIN (Simplificado) ---
if "logado" not in st.session_state: st.session_state["logado"] = False

if not st.session_state["logado"]:
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar") and senha == "1234":
        st.session_state["logado"] = True
        st.rerun()
else:
    # Buscar dados
    response = supabase.table("prestadores").select("*").execute()
    prestadores = response.data

    # Tabela
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    c1.write("**Prestador**"); c2.write("**Referência**")
    c3.write("**Pagamento**"); c4.write("**Tempo Restante**")

    for p in prestadores:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        col1.write(p['nome_prestador'])
        col2.write(p.get('referencia_pagamento', ''))
        
        status = p['status_pagamento']
        inicio_str = p.get('inicio_servico')
        
        if status and inicio_str:
            inicio = datetime.fromisoformat(inicio_str.replace('Z', '+00:00'))
            agora = datetime.now(timezone.utc)
            restante = 7200 - (agora - inicio).total_seconds()

            if restante > 0:
                m, s = divmod(int(restante), 60)
                col3.write("✅ SIM")
                col4.write(f"⏳ {m:02d}m {s:02d}s")
            else:
                # Expira automaticamente
                supabase.table("prestadores").update({"status_pagamento": False, "inicio_servico": None}).eq("id", p['id']).execute()
                st.rerun()
        else:
            col3.write("❌ NÃO")
            if col4.button("Pagar", key=f"btn_{p['id']}"):
                supabase.table("prestadores").update({
                    "status_pagamento": True, 
                    "inicio_servico": datetime.now(timezone.utc).isoformat()
                }).eq("id", p['id']).execute()
                st.rerun()
