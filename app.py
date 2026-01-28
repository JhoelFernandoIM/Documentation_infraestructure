import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

st.title("🔐 Iniciar Sesión")

with st.form("login_form"):
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    submit = st.form_submit_button("Ingresar")

if submit:
    st.info("Login visual funcionando (sin validar aún)")
