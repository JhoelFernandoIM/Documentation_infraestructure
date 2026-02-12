import streamlit as st
import os
from src.db.supabase_client import *
from src.services.word_generator import generar_validacion
from src.utils.formatters import format_4_digits, format_6_digits


st.set_page_config(page_title="Validacion", layout="wide")

st.title("📄 Generar Hoja de Coordinación - Validación")
st.divider()


#selecionar documentos

documentos = obtener_documentos_full()

doc_dict = {
    d["nombre_doc"]: d
    for d in documentos
}

doc_sel = st.selectbox(
    "Seleccionar documento de referencia",
    list(doc_dict.keys())
)

#formulario

with st.form("form_hoja"):

    numero_doc = st.number_input("Número de hoja", min_value=1, step=1)

    tipo_pedido = st.selectbox(
        "Tipo de pedido",
        ["SERVICIO", "COMPRA"]
    )

    num_pedido = st.number_input("Número de pedido", min_value=1, step=1)

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

    try:
        locale.setlocale(locale.LC_TIME, "es_PE.UTF-8")
    except:
        try:
            locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        except:
            pass

    fecha_actual = fecha_actual_input.strftime("%d de %B de %Y")

    numero_doc_fmt = format_4_digits(numero_doc)
    num_pedido_fmt = format_6_digits(num_pedido)

    contexto = {
        "numero_doc": numero_doc_fmt,
        "tipo_pedido": tipo_pedido,
        "num_pedido": num_pedido_fmt,
        "nombre_obra": nombre_obra,
        "num_cui": obra_data["cui"],
        "nombre_doc": doc_sel,
        "nombre_resi": nombre_resi,
        "nombre_super": nombre_super,
        "responsable_control": responsable_control,
        "fecha_actual": fecha_actual
    }

    output_file = f"generated_docs/HC_{numero_doc_fmt}.docx"

    if not os.path.exists("generated_docs"):
        os.makedirs("generated_docs")

    generar_validacion(contexto, output_file)

    with open(output_file, "rb") as f:
        st.download_button(
            "📥 Descargar Hoja de Coordinación",
            f,
            file_name=f"HC_{numero_doc_fmt}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    st.success("Documento generado correctamente")
