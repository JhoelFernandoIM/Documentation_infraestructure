import streamlit as st
from datetime import date
from src.db.supabase_client import *
import pandas as pd

st.set_page_config(page_title="Registro de Documentos", layout="wide")

st.title("📑 Registro de Documentos")
st.divider()


#selección de interesados

# selección de interesados

interesados = obtener_interesados_combo()
inter_dict = {i["nombre_rs"]: i for i in interesados}

opciones = ["-- Seleccione interesado --"] + list(inter_dict.keys())

nombre_interesado = st.selectbox(
    "Seleccionar interesado",
    opciones
)

# Solo definir datos si realmente seleccionó
if nombre_interesado != "-- Seleccione interesado --":
    inter_data = inter_dict[nombre_interesado]
    tipo_interesado = inter_data["tipo_interesado"]
    id_interesado = inter_data["id_interesado"]
else:
    tipo_interesado = None
    id_interesado = None



#generar sigla
def generar_sigla(nombre):
    palabras = nombre.split()
    sigla = "".join([p[0].upper() for p in palabras if len(p) >= 3])
    return sigla

#crear nombre doc

def construir_nombre_doc(
    tipo_doc,
    correlativo,
    anio,
    sigla_gerencia,
    sigla_subgerencia,
    tercer_nivel,
    nombre_interesado
):

    sigla_nombre = generar_sigla(nombre_interesado)

    partes_area = []

    if sigla_gerencia:
        partes_area.append(sigla_gerencia)

    if sigla_subgerencia:
        partes_area.append(sigla_subgerencia)

    if tercer_nivel:
        partes_area.append(tercer_nivel)

    bloque_area = "/".join(partes_area)

    nombre = (
        f"{tipo_doc} Nº {correlativo}-{anio}-MDSM/"
        f"{bloque_area}-{sigla_nombre}"
    )

    return nombre


#formulario
with st.form("form_documento"):

    col1, col2 = st.columns(2)

    with col1:
        tipo_mov = st.selectbox(
            "Tipo de movimiento",
            ["ENTRADA", "SALIDA"]
        )

        tipo_doc = st.selectbox(
            "Tipo de documento",
            [
                "INFORME",
                "MEMORANDUM",
                "MEMORANDUM MULTIPLE",
                "REQUERIMIENTO",
                "HOJA DE COORDINACION",
                "TRAMITE DOCUMENTARIO"
            ]
        )

        num_correlativo = st.text_input(
            "Número correlativo",
        )

        anio = st.number_input(
            "Año",
            value=2026,
            step=1
        )

    with col2:
        fecha_reg = st.date_input(
            "Fecha de registro",
            value=date.today()
        )

        num_asiento = st.number_input(
            "Número de asiento",
            min_value=1,
            step=1
        )

    #si es obra
    if tipo_interesado == "PERSONAL_OBRA":

        sigla_gerencia = "GDTI"
        sigla_subgerencia = "SGI"

        personal = obtener_personal_obra_por_interesado(id_interesado)

        if personal:
            rol = personal[0]["rol_obra"]
            tercer_nivel = generar_sigla(rol)
            st.info(f"Cargo detectado: {rol}")
        else:
            tercer_nivel = None
            st.warning("No se encontró rol de obra para este interesado")


#si es municipal
    elif tipo_interesado == "AREA_MUNICIPAL":

        areas_funcionario = obtener_area_por_interesado(id_interesado)

        if areas_funcionario:

            area_funcionario = areas_funcionario[0]
            nivel_funcionario = area_funcionario["nivel"]
            nombre_area_funcionario = area_funcionario["nombre_area"]

            st.info(f"Funcionario pertenece a nivel {nivel_funcionario}")

            sigla_gerencia = None
            sigla_subgerencia = None
            tercer_nivel = None

            # =========================
            # SI ES NIVEL 1
            # =========================

            if nivel_funcionario == 1:

                sigla_gerencia = generar_sigla(nombre_area_funcionario)


            # =========================
            # SI ES NIVEL 2
            # =========================

            elif nivel_funcionario == 2:

                # Elegir nivel 1
                areas_n1 = obtener_areas_por_nivel(1)
                opciones_n1 = {a["nombre_area"]: a for a in areas_n1}

                nombre_n1 = st.selectbox(
                    "Seleccionar Gerencia (Nivel 1)",
                    list(opciones_n1.keys())
                )

                sigla_gerencia = generar_sigla(nombre_n1)

                # Nivel 2 es el propio
                sigla_subgerencia = generar_sigla(nombre_area_funcionario)


            # =========================
            # SI ES NIVEL 3
            # =========================

            elif nivel_funcionario == 3:

                # Elegir nivel 1
                areas_n1 = obtener_areas_por_nivel(1)
                opciones_n1 = {a["nombre_area"]: a for a in areas_n1}

                nombre_n1 = st.selectbox(
                    "Seleccionar Gerencia (Nivel 1)",
                    list(opciones_n1.keys())
                )

                sigla_gerencia = generar_sigla(nombre_n1)

                # Elegir nivel 2
                areas_n2 = obtener_areas_por_nivel(2)
                opciones_n2 = {a["nombre_area"]: a for a in areas_n2}

                nombre_n2 = st.selectbox(
                    "Seleccionar Subgerencia (Nivel 2)",
                    list(opciones_n2.keys())
                )

                sigla_subgerencia = generar_sigla(nombre_n2)

                # Nivel 3 es el propio
                tercer_nivel = generar_sigla(nombre_area_funcionario)
    

#si es externo
    else:
        sigla_gerencia = None
        sigla_subgerencia = None
        tercer_nivel = None

    guardar = st.form_submit_button("Registrar Documento")

#fuera del form
if guardar:

    nombre_documento = construir_nombre_doc(
        tipo_doc,
        num_correlativo,
        anio,
        sigla_gerencia,
        sigla_subgerencia,
        tercer_nivel,
        nombre_interesado
    )


    data_doc = {
        "tipo_movimiento": tipo_mov,
        "tipo_documento": tipo_doc,
        "num_correlativo": num_correlativo,
        "anio": anio,
        "sigla_gerencia": sigla_gerencia,
        "sigla_subgerencia": sigla_subgerencia,
        "id_interesado": id_interesado,
        "fecha_registro": fecha_reg.isoformat(),
        "num_asiento": num_asiento,
        "tercer_nivel": tercer_nivel,
        "nombre_doc": nombre_documento
    }

    insertar_documento(data_doc)

    st.success("Documento registrado correctamente")


#visualizar:
st.divider()
st.subheader("📋 Vista detallada de documentos")

documentos = obtener_documentos_full()

documentos = obtener_documentos_full()

if documentos:
    df = pd.DataFrame(documentos)

    df["nombre_interesado"] = df["remitente"].apply(lambda x: x["nombre_rs"])
    df["tipo_interesado"] = df["remitente"].apply(lambda x: x["tipo_interesado"])

    # Extraer nombre de obra si existe
    def obtener_obra(rem):
        try:
            return rem["personal_obra"][0]["obra"]["nombre_obra"]
        except (TypeError, KeyError, IndexError):
            return ""


    df["obra"] = df["remitente"].apply(obtener_obra)

    df = df.drop(columns=["remitente"])

else:
    df = pd.DataFrame()

#crear tablas
tab1, tab2, tab3, tab4 = st.tabs([
    "Todos",
    "Personal de obra",
    "Área municipal",
    "Externos"
])

with tab1:
    if not df.empty:
        st.dataframe(
            df[[
                "num_asiento",
                "fecha_registro",
                "nombre_doc",
                "tipo_interesado"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay registros")

with tab2:
    df_po = df[df["tipo_interesado"] == "PERSONAL_OBRA"]

    if not df_po.empty:
        st.dataframe(
            df_po[[
                "num_asiento",
                "fecha_registro",
                "nombre_doc",
                "obra"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay documentos de personal de obra")


with tab3:
    df_area = df[df["tipo_interesado"] == "AREA_MUNICIPAL"]

    if not df_area.empty:
        st.dataframe(
            df_area[[
                "num_asiento",
                "fecha_registro",
                "nombre_doc"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay documentos de área municipal")

with tab4:
    df_ext = df[df["tipo_interesado"] == "EXTERNO"]

    if not df_ext.empty:
        st.dataframe(
            df_ext[[
                "num_asiento",
                "fecha_registro",
                "nombre_doc"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay documentos externos")
