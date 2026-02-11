import streamlit as st
import pandas as pd

from src.db.supabase_client import insertar_obra, obtener_obras
from src.utils.validators import validar_obra

#personalización

st.set_page_config(page_title="Módulo de Obras", layout="wide")

st.markdown("<h1>🏗️ Gestión de Obras</h1>", unsafe_allow_html=True)
st.divider()


with st.expander("➕ Registrar nueva obra", expanded=True):
    with st.form("form_obra"):
        
        nombre_obra = st.text_area("Nombre de la obra")
        
        col1, col2 = st.columns(2)


        with col1:
            codigo_obra = st.text_input("Código único de inversiones (CUI)")
            tipo_obra = st.selectbox(
                "Cadena Funcional",
                ["Ambiente", "Transporte", "Educación","Cultura y Deporte", "Saneamiento", "Mantenimiento"]
            )
            presupuesto = st.number_input(
                "Presupuesto (S/.)",
                min_value=0.0,
                step=1000.0
            )


        with col2:
            res_aprob_exp = st.text_input("Resolución de aprobación de expediente")
            res_aprob_ejec = st.text_input("Resolución de aprobación de ejecución de obra")

            modalidad_ejec =st.selectbox(
                "Modalidad de ejecución",
                ["OAD (Administración directa)", "OAI (Contrata)"]
            )

            meta = st.number_input(
                "Meta",
                min_value=0,
                step=1
            )

        observaciones = st.text_area("Observaciones")

        btn_guardar = st.form_submit_button("💾 Registrar obra")

    if btn_guardar:
        valido, mensaje = validar_obra(nombre_obra, presupuesto)

        if not valido:
            st.error(mensaje)
        else:
            data_obra = {
                "cui": codigo_obra,
                "nombre_obra": nombre_obra,
                "cad_funcion": tipo_obra,
                "presupuesto": presupuesto,
                "resolucion_aprob_exp": res_aprob_exp,
                "resolucion_aprob_ejec": res_aprob_ejec,
                "modalidad_ejec": modalidad_ejec,
                "meta": meta,
                "observaciones": observaciones
            }

            insertar_obra(data_obra)
            st.success("✅ Obra registrada correctamente")


#tabla

st.subheader("📋 Resumen de obras registradas")

obras = obtener_obras()

if obras:
    df = pd.DataFrame(obras)

    df = df[[
        "id_obra",
        "cui",
        "nombre_obra",
        "cad_funcion",
        "modalidad_ejec",
        "presupuesto",
        "meta"
    ]]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No hay obras registradas")

