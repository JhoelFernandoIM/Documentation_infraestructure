from docxtpl import DocxTemplate
import os

def generar_validacion(contexto, output_path):
    template_path = "templates/hoja_coordinacion_validacion.docx"

    doc = DocxTemplate(template_path)
    doc.render(contexto)
    doc.save(output_path)

    return output_path


def generar_conformidad(contexto, output_path):
    template_path = "templates/informe_conformidad.docx"

    doc = DocxTemplate(template_path)
    doc.render(contexto)
    doc.save(output_path)

    return output_path
