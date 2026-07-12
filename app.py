import streamlit as st

# Senha de Administrador
ADMIN_PASSWORD = "sua_senha_secreta"

def login():
    senha = st.text_input("Digite a senha de ADMIN:", type="password")
    if senha == ADMIN_PASSWORD:
        return True
    return False

st.title("Painel de Controle - Administração")

if login():
    st.success("Bem-vindo, Administrador!")
    
    # Aqui você vai puxar a lista de prestadores do seu banco de dados Supabase
    # Exemplo visual:
    dados_prestadores = [
        {"nome": "João Karaoke", "referencia": "REF123", "pago": False},
        {"nome": "Maria Som", "referencia": "REF456", "pago": True}
    ]
    
    for p in dados_prestadores:
        col1, col2, col3 = st.columns(3)
        col1.write(p['nome'])
        col2.write(p['referencia'])
        if st.checkbox(f"Confirmar Pagamento {p['nome']}", value=p['pago']):
            st.write("Status: LIBERADO")
        else:
            st.warning("Pendente")
else:
    st.error("Acesso restrito. Insira a senha.")
