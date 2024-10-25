import re
from plistlib import InvalidFileException
from tkinter import messagebox
import json
import unicodedata
from docx import Document
from docx2pdf import convert

from window.GUI_Builders import topmost_messagebox
from window.form.export_window import SheetWriter


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def leer_datos(form):

    """
    Esta función se usa para retornar los datos de todos los campos del formulario y los devuelve en forma de dict.

    """

    datos = {
        "FICHA": f"FICHA N°{form.ficha.get()}",
        "EDICION": f"EDICION N°{form.edicion.get()}",
        "REVISION": f"REVISION: {form.fecha_revision.get_date()}",
        "VIGENTE": f"VIGENTE: {form.vigente.get_date()}",
        "RESPONSABLE": f"REVISADO POR: {form.responsable.get()}",
        "NOMBRE": form.nombre_producto.get(),
        "ESTADO": form.forma.get(),
        "SGA": form.lista_sga,
        "EPP": form.lista_epp,
        "RIESGOS": form.text_riesgos.get("1.0", "end"),
        "MANIPULACION": form.text_manipulacion.get("1.0", "end"),
        "ALMACENAMIENTO": form.text_almacenamiento.get("1.0", "end"),
        "ELIMINACION": form.text_eliminacion.get("1.0", "end"),

        "FIRSTAID": form.text_firstaid.get("1.0", "end"),
        "DERRAME": form.text_derrame.get("1.0", "end"),
        "FUEGO": form.text_fuego.get("1.0", "end")

    }

    return datos

def to_json(datos):
    filename = slugify(datos["NOMBRE"])
    print(filename)
    with open(f"raw-{filename}.json", "w") as json_file:
        json.dump(datos, json_file, indent=4)

def exportar(form, output_path):
    """
    Se leen los datos del formulario y se crea una hoja de word usando SheetWriter.
    """
    print("GENERANDO...")

    datos = leer_datos(form)
    doc = Document("template.docx")

    # Replace the placeholder with the name from the form data
    SheetWriter.fill_form(doc, datos)

    # Define the output paths
    filename = slugify(datos["NOMBRE"])
    word_file_path = f"{output_path}/{filename}.docx"
    pdf_file_path = f"{output_path}/{filename}.pdf"

    # Save the Word document
    doc.save(word_file_path)

    # Convert to PDF
    #convert(word_file_path, pdf_file_path)

    print("Document saved as PDF and opened:", pdf_file_path)


def cargar_datos(form):
    print("CARGANDO")

def guardar_datos(form):
    to_json(leer_datos(form))


    # Muestra los datos guardados
    topmost_messagebox("Datos Exportados", "Se exportaron los datos correctamente.")