from tkinter import messagebox

from docx import Document
from docx2pdf import convert

from window.form.export_window import SheetWriter


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
        "SGA": [f"assets/sga/{form.sga_descripciones[i][0:1]}.png" for i in range(len(form.sga_descripciones))
                if form.lista_sga[i].get() == 1],
        "EPP": [f"assets/epp/{form.epp_descripciones[i][0:1]}.png" for i in range(len(form.epp_descripciones))
                if form.lista_sga[i].get() == 1],
        "RIESGOS": form.text_riesgos.get("1.0", "end"),
        "MANIPULACION": form.text_manipulacion.get("1.0", "end"),
        "ALMACENAMIENTO": form.text_almacenamiento.get("1.0", "end"),
        "ELIMINACION": form.text_eliminacion.get("1.0", "end"),

        "FIRSTAID": form.text_firstaid.get("1.0", "end"),
        "DERRAME": form.text_derrame.get("1.0", "end"),
        "FUEGO": form.text_fuego.get("1.0", "end")

    }

    return datos


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
    word_file_path = f"{output_path}/{datos['NOMBRE']}.docx"
    pdf_file_path = f"{output_path}/{datos['NOMBRE']}.pdf"

    # Save the Word document
    doc.save(word_file_path)

    # Convert to PDF
    #convert(word_file_path, pdf_file_path)

    print("Document saved as PDF and opened:", pdf_file_path)


def cargar_datos(form):
    print("CARGANDO")

def guardar_datos(form):

    datos = leer_datos(form)
    for key in datos:
            print(key, ':', datos[key])


    # Muestra los datos guardados
    messagebox.showinfo("Guardado", f"Se guardaron los datos ingresados.")