import streamlit as st
from src.db.supabase_client import *
import pandas as pd

st.title("Registro de Interesados")

obras = obtener_obras_combo()
obras_dict = {o["nombre_obra"]: o["id_obra"] for o in obras}


tipo = st.selectbox(
        "Tipo interesado",
        ["PERSONAL_OBRA", "AREA_MUNICIPAL", "EXTERNO"],
        key="tipo_interesado"
    )

with st.form("form_interesado"):

    nombre = st.text_input("Nombre / Razón social")
    documento = st.text_input("Número de Documento")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")

    

    if st.session_state.tipo_interesado == "PERSONAL_OBRA":
        obra_sel = st.selectbox("Obra", list(obras_dict.keys()))
        rol_obra = st.text_input("Rol en obra")

    elif st.session_state.tipo_interesado == "AREA_MUNICIPAL":
        nombre_area = st.text_input("Nombre del área")
        nivel = st.number_input("Nivel", min_value=1, step=1)

    elif st.session_state.tipo_interesado == "EXTERNO":
        tipo_entidad = st.text_input("Tipo de entidad")

    guardar = st.form_submit_button("Guardar")

if guardar:

    remitente_data = {
        "tipo_interesado": tipo,
        "nombre_rs": nombre,
        "num_documento": documento,
        "telefono": telefono,
        "correo": correo
    }

    nuevo = insertar_remitente(remitente_data)
    id_interesado = nuevo["id_interesado"]

    if tipo == "PERSONAL_OBRA":
        insertar_personal_obra({
            "id_interesado": id_interesado,
            "id_obra": obras_dict[obra_sel],
            "rol_obra": rol_obra
        })

    if tipo == "AREA_MUNICIPAL":
        insertar_area_municipal({
            "id_interesado": id_interesado,
            "nombre_area": nombre_area,
            "nivel": nivel
        })

    if tipo == "EXTERNO":
        insertar_entidad_externa({
            "id_interesado": id_interesado,
            "tipo_entidad": tipo_entidad
        })

    st.success("Interesado registrado correctamente")


#tabla
st.divider()
st.subheader("📋 Lista de interesados")


interesados = obtener_interesados_full()


df = pd.DataFrame(interesados)

if df.empty:
    st.warning("No hay interesados registrados aún")
    st.stop()


#filtros
col1, col2 = st.columns(2)

with col1:
    filtro_tipo = st.selectbox(
        "Filtrar por tipo",
        ["TODOS", "PERSONAL_OBRA", "AREA_MUNICIPAL", "EXTERNO"]
    )

df_filtrado = df.copy()

if filtro_tipo != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["tipo_interesado"] == filtro_tipo]


df_filtrado = df_filtrado[[
    "id_interesado",
    "tipo_interesado",
    "nombre_rs",
    "num_documento",
    "telefono",
    "correo"
]]

#mostrar tabla
st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

#botnoes
col1, col2, col3 = st.columns(3)

if col1.button("Ver personal de obra"):
    st.session_state.filtro_tipo = "PERSONAL_OBRA"

if col2.button("Ver área municipal"):
    st.session_state.filtro_tipo = "AREA_MUNICIPAL"

if col3.button("Ver externos"):
    st.session_state.filtro_tipo = "EXTERNO"
