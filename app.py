import streamlit as st
from src.db.supabase_client import get_supabase_client

st.set_page_config(page_title="Login", layout="centered")

#CSS
st.markdown("""
<style>
/* Fondo general */
.stApp {
    background-color: #f4f6f8;
}

/* Título */
h1,h2 {
    color: #0b5394;
    text-align: center;
}
            
/* Botón */
.stButton > button {
    background-color: #0b5394;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-weight: bold;
}

/* Inputs */
input {
    border-radius: 6px !important;
}

/* Centrar formulario */
[data-testid="stForm"] {
    background-color: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
            
                                  
</style>
""", unsafe_allow_html=True)





col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.image("assets/images/logo_san_miguel.jpg", width=120)
    st.caption("Municipalidad Distrital de San Miguel")

with col2:
    st.title("Documentación - Infraestructura")
    st.header("Iniciar Sesión")

with col3:
    st.image("assets/images/logo_san_miguel.jpg", width=120)
    st.caption("Municipalidad Distrital de San Miguel")

supabase = get_supabase_client()

with st.form("login_form"):
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    submit = st.form_submit_button("Ingresar")

if submit:
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if response.user:
        st.session_state["user"] = response.user
        st.session_state["session"] = response.session
        st.success("Login exitoso")

        if "session" in st.session_state:
            supabase.postgrest.auth(
                st.session_state["session"].access_token
            )

            data = supabase.table("documentos").select("*").execute()
            st.write(data.data)

    else:
        st.error("Credenciales incorrectas")
