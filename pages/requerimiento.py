import streamlit as st
import os
from src.db.supabase_client import *
from src.services.word_generator import generar_requerimiento
from src.utils.formatters import format_4_digits, format_6_digits


st.set_page_config(page_title="Requerimiento", layout="wide")

st.title("📄 Generar Requerimiento")
st.divider()


#selecionar documentos

documentos = obtener_documentos_full()

doc_dict = {
    d["nombre_doc"]: d
    for d in documentos
}

#nuevo
doc_sel = st.selectbox(
    "Seleccionar documento de referencia",
    list(doc_dict.keys())
)

# Permitir editar el nombre
doc_editable = st.text_input(
    "Editar nombre del documento (opcional)",
    value=doc_sel
)

#formulario

with st.form("form_hoja"):

    numero_doc = st.number_input("Número de Requerimiento ", min_value=1, step=1)

    tipo_pedido = st.selectbox(
        "Tipo de pedido",
        ["SERVICIO", "COMPRA"]
    )

    num_pedido = st.number_input("Número de pedido", min_value=1, step=1)

    # NUEVO CAMPO
    producto = st.text_input("Producto o servicio solicitado")

    # Obras
    obras = obtener_obras_combo()
    obras_dict = {o["nombre_obra"]: o for o in obras}

    nombre_obra = st.selectbox(
        "Seleccionar obra",
        list(obras_dict.keys())
    )
    #previa

# Vista previa automática del personal
    obra_data = obras_dict[nombre_obra]
    id_obra = obra_data["id_obra"]

    personal = obtener_personal_por_obra(id_obra)

    nombre_resi = ""
    nombre_super = ""

    for p in personal:

        rol = p.get("rol_obra", "").upper()
        remitente = p.get("remitente")

        if not remitente:
            continue

        nombre = remitente.get("nombre_rs", "")
        prefijo = remitente.get("prefijo_prof", "")

        if prefijo:
            nombre_completo = f"{prefijo}. {nombre}".upper()
        else:
            nombre_completo = nombre.upper()

        if "RESIDENTE" in rol:
            nombre_resi = nombre_completo

        elif "SUPERVISOR" in rol or "INSPECTOR" in rol:
            nombre_super = nombre_completo



    st.markdown("### 👷 Vista previa personal de obra")

    st.write("**Residente:**", nombre_resi if nombre_resi else "No asignado")
    st.write("**Supervisor / Inspector:**", nombre_super if nombre_super else "No asignado")


    #hasta aqui

    responsable_control = st.selectbox(
        "Responsable de control",
        ["inspector de obra", "supervisor de obra"]
    )


    #fecha

    from datetime import date
    import locale

    # Fecha editable con valor por defecto actual
    fecha_actual_input = st.date_input(
        "Fecha del documento",
        value=date.today()
    )


    generar = st.form_submit_button("Generar documento")


# ==============================
# LOGICA DE GENERACION
# ==============================

if generar:

    #nuevo
    doc_data = doc_dict[doc_sel]

    fecha_doc = doc_data.get("fecha_registro")

    from datetime import datetime

    fecha_recepcion = ""

    if fecha_doc:
        fecha_dt = datetime.strptime(fecha_doc, "%Y-%m-%d")

        MESES_ES = {
            1: "enero", 2: "febrero", 3: "marzo",
            4: "abril", 5: "mayo", 6: "junio",
            7: "julio", 8: "agosto", 9: "septiembre",
            10: "octubre", 11: "noviembre", 12: "diciembre"
        }

        fecha_recepcion = f"{fecha_dt.day} de {MESES_ES[fecha_dt.month]} de {fecha_dt.year}"


    obra_full = obtener_obra_por_id(id_obra)

    reso_expediente = obra_full.get("resolucion_aprob_exp", "")
    fecha_reso_expediente = obra_full.get("fecha_r_expediente", "")

    reso_ejecucion = obra_full.get("resolucion_aprob_ejec", "")
    fecha_reso_ejecucion = obra_full.get("fecha_r_ejecucion", "")

    def formatear_fecha_es(fecha_str):
        if not fecha_str:
            return ""

        fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")

        MESES_ES = {
            1: "enero", 2: "febrero", 3: "marzo",
            4: "abril", 5: "mayo", 6: "junio",
            7: "julio", 8: "agosto", 9: "septiembre",
            10: "octubre", 11: "noviembre", 12: "diciembre"
        }

        return f"{fecha_dt.day} de {MESES_ES[fecha_dt.month]} de {fecha_dt.year}"

    fecha_reso_expediente = formatear_fecha_es(fecha_reso_expediente)
    fecha_reso_ejecucion = formatear_fecha_es(fecha_reso_ejecucion)

    meta = obra_full.get("meta", "")
    num_meta = str(meta).zfill(4) if meta else "0000"



    #nuevo

    obra_data = obras_dict[nombre_obra]
    id_obra = obra_data["id_obra"]

    personal = obtener_personal_por_obra(id_obra)

    nombre_resi = ""
    nombre_super = ""

    for p in personal:

        rol = p.get("rol_obra", "").upper()
        remitente = p.get("remitente")

        if not remitente:
            continue

        nombre = remitente.get("nombre_rs", "")
        prefijo = remitente.get("prefijo_prof", "")

        # Formato: ING. NOMBRE COMPLETO
        if prefijo:
            nombre_completo = f"{prefijo}. {nombre}".upper()
        else:
            nombre_completo = nombre.upper()

        # Detectar roles correctamente aunque digan:
        # "Residente de obra", "Supervisor de obra", etc.
        if "RESIDENTE" in rol:
            nombre_resi = nombre_completo

        elif "SUPERVISOR" in rol or "INSPECTOR" in rol:
            nombre_super = nombre_completo

    # ==============================
    # RESPONSABLE SEGUN SELECTBOX
    # ==============================

    if "inspector" in responsable_control.lower():
        responsable_final = nombre_super
    else:
        responsable_final = nombre_super

    # ==============================
    # FECHA EN ESPAÑOL
    # ==============================

    # ==============================
    # FECHA EN ESPAÑOL (SIN LOCALE)
    # ==============================

    MESES_ES = {
        1: "enero", 2: "febrero", 3: "marzo",
        4: "abril", 5: "mayo", 6: "junio",
        7: "julio", 8: "agosto", 9: "septiembre",
        10: "octubre", 11: "noviembre", 12: "diciembre"
    }

    dia = fecha_actual_input.day
    mes = MESES_ES[fecha_actual_input.month]
    anio = fecha_actual_input.year

    fecha_actual = f"{dia} de {mes} de {anio}"


    numero_doc_fmt = format_4_digits(numero_doc)
    num_pedido_fmt = format_6_digits(num_pedido)

    contexto = {
        "numero_doc": numero_doc_fmt,
        "tipo_pedido": tipo_pedido,
        "num_pedido": num_pedido_fmt,
        "nombre_obra": nombre_obra,
        "num_cui": obra_data["cui"],
        "nombre_doc": doc_editable,
        "nombre_resi": nombre_resi,
        "nombre_super": nombre_super,
        "responsable_control": responsable_control,
        "producto": producto,
        "fecha_actual": fecha_actual,
        "fecha_recepcion": fecha_recepcion,
        #nuevo
        "reso_expediente": reso_expediente,
        "fecha_reso_expediente": fecha_reso_expediente,
        "reso_ejecucion": reso_ejecucion,
        "fecha_reso_ejecucion": fecha_reso_ejecucion,
        "num_meta": num_meta
    }

    output_file = f"generated_docs/REQ_{numero_doc_fmt}.docx"

    if not os.path.exists("generated_docs"):
        os.makedirs("generated_docs")

    generar_requerimiento(contexto, output_file)

    with open(output_file, "rb") as f:
        st.download_button(
            "📥 Descargar REQUERIMIENTO",
            f,
            file_name=f"REQUERIMIENTO N° {numero_doc_fmt}  {producto}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    st.success("Documento generado correctamente")
