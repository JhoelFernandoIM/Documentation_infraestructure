import streamlit as st
from src.db.supabase_client import *
import pandas as pd

st.title("🧑‍💼 Registro de Interesados")

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

st.divider()
st.subheader("Vistas detalladas")

tab1, tab2, tab3, tab4 = st.tabs([
    "Todos",
    "Personal de obra",
    "Área municipal",
    "Externos"
])

with tab1:
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

with tab2:
    personal = obtener_personal_obra_full()
    if personal:
        df_po = pd.DataFrame(personal)
        st.dataframe(df_po, use_container_width=True)
    else:
        st.info("No hay personal de obra")

with tab3:
    area = obtener_area_municipal_full()
    if area:
        df_area = pd.DataFrame(area)
        st.dataframe(df_area, use_container_width=True)
    else:
        st.info("No hay áreas registradas")

with tab4:
    ext = obtener_externos_full()
    if ext:
        df_ext = pd.DataFrame(ext)
        st.dataframe(df_ext, use_container_width=True)
    else:
        st.info("No hay entidades externas")

