from pathlib import Path
from tkinter import ttk, messagebox

import tkcalendar

from window.form import FormIO
from window.form.FileBrowser import FileBrowser
from window.form.export_window.ExportWindow import ExportWindow
from window.GUI_Builders import *

"""
Ventana principal de formulario de producto:
Aquí se puede diseñar la ventana de formulario principal. 
El código está organizado para que hayan grupos de Widgets. 
De este modo, se evita repetir código boilerplate y se puede especificar 
posiciones relativas entre los widgets del grupo y el origen del grupo (x,y)

Al ejecutar una acción de guardado, el módulo FormIO leerá los datos. 
Allí se debe modificar los datos a ser leeidos en su función leer_datos() en caso de añadir nuevos campos.
"""


class ProductoFormulario:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario de Producto Químico")
        self.root.geometry("1920x1080")

        # Initialize variables
        self.init_variables()

        # Create UI components
        self.crear_header()
        self.crear_secciones()
        self.browser = FileBrowser(self, x=1050, y=120, width=580, height=860)
    def init_variables(self):
        self.docx_output_path = "No hay carpeta seleccionada."

        self.ficha = tk.IntVar(self.root)
        self.edicion = tk.IntVar(self.root)
        self.nombre_producto = tk.StringVar(self.root)
        self.grupo_quimico = tk.StringVar(self.root)
        self.forma = tk.StringVar(self.root)
        self.responsable = tk.StringVar(self.root)

        self.sga_descripciones = [
            "1 - Explosivo", "2 - Inflamable, Combustible", "3 - Comburente, Oxidante",
            "4 - Gas presurizado", "5 - Corrosivo", "6 - Tóxico",
            "7 - irritante, narcótico",
            "8 - Carcinógeno, mutágeno",
            "9 - Dañino p/ medio ambiente"
        ]
        self.epp_descripciones = [
            "1 - Guantes de Seguridad", "2 - Mascara respiratoria", "3 - Gafas de Seguridad"
        ]
        self.lista_sga = []
        self.lista_epp = []

        self.buttons_sga = []
        self.buttons_epp = []




    """
    Parameters for helper functions:
    NOTE: Positions (x,y) are relative to the group's origin.
    
    - char_limit: The character limit for the inputs.
    - x_origin: The x-coordinate for the group's origin. 
    - y_origin: The y-coordinate for the group's origin.
    - label_text (str): The text to display on the label.
    - var (tk.Variable): The tkinter variable (IntVar, StringVar, etc.) associated with the entry or checkbox.
    - lx (int): The x-coordinate for placing the label.
    - ly (int): The y-coordinate for placing the label.
    - width (int): The width of the entry or button.
    - ex (int): The x-coordinate for placing the entry widget.
    - ey (int): The y-coordinate for placing the entry widget.
    - text (str): The text to display on the button.
    - command (function): The function to call when the button is clicked.
    - x (int): The x-coordinate for placing the button.
    - y (int): The y-coordinate for placing the button.
    - descriptions (list): A list of descriptions for each checkbox.
    - var_array (list): A list of tkinter variable (IntVar) for each checkbox.
    - var: A variable where the widget or its contents will be stored
    - cy_start (int): The starting y-coordinate for placing the checkboxes.
    - tx (int): The x-coordinate for placing the text widget.
    - ty (int): The y-coordinate for placing the text widget.
    - sx (int): The x-coordinate for placing the scrollbar.
    - sh (int): The height of the scrollbar.
    - dx (int): The x-coordinate for placing the date entry widget.
    - dy (int): The y-coordinate for placing the date entry widget.
    """

    def crear_header(self):
        """Creates the header section with basic product information."""
        crear_entry(self.root, 10, 10, "Forma / Estado:", self.forma, 55, 0, 0, 30, 0, 20)
        crear_entry(self.root, 195, 10, "Nombre del Producto:", self.nombre_producto, 64, 0, 0, 50, 0, 20)
        crear_entry(self.root, 10, 50, "Responsable de Revisión:", self.responsable, 55, 0, 0, 81, 0, 20)

        crear_entry(self.root, 510, 10, "Edición N°", self.edicion, 4, 0, 0, 13, 0, 20)
        crear_entry(self.root, 595, 10, "Ficha N°", self.ficha, 4, 0, 0, 13, 0, 20)
        self.fecha_revision = crear_date_entry(self.root, 510, 50, "Revisión:", 0, 0, 0, 20)
        self.vigente = crear_date_entry(self.root, 595, 50, "Vigente:", 0, 0, 0, 20)

        # Botones principales
        crear_boton(self.root, "Abrir opciones de Exportación", lambda: ExportWindow(self) , 750, 45, 200)

    def crear_secciones(self):
        """Creates all sections of the form (Pictograms, EPP, Text fields)."""
        # Separador
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', pady=95)

        # Secciones de texto
        self.text_riesgos = crear_text_section(self.root, 10, 100, "Riesgos del Producto", 680, 0, 0, 20, 20, 0, 210)
        self.text_manipulacion = crear_text_section(self.root, 350, 100, "Consignas de Manipulación Segura", 800, 0, 0, 20,
                                 20, 0, 210)

        self.text_almacenamiento = crear_text_section(self.root, 10, 335, "Consignas de Almacenamiento Seguro", 800, 0, 0, 20,
                                 20, 0, 210)

        self.text_eliminacion = crear_text_section(self.root, 350, 335, "Consignas de Eliminación o Desecho", 800, 0, 0, 20,
                                 20, 0, 210)

        self.text_firstaid = crear_text_section(self.root, 10, 570, "Primeros Auxilios", 900, 0, 0,
                                                   20,
                                                   20, 0, 150, width=107, height=12)

        self.text_derrame = crear_text_section(self.root, 10, 765, "En caso de Derrame", 800, 0, 0,
                                                   20,
                                                   20, 0, 210)

        self.text_fuego = crear_text_section(self.root, 350, 765, "En caso de Fuego", 800, 0, 0,
                                                   20,
                                                   20, 0, 210)

        sga_buttons_origin = [700, 120]
        button_width, button_height = 100, 140
        x_offset, y_offset = 105, 145  # Distance between buttons

        for i in range(9):
            row = i // 3  # Determine the row (0, 1, or 2)
            col = i % 3  # Determine the column (0, 1, or 2)

            x = col * x_offset  # Calculate x position
            y = row * y_offset  # Calculate y position
            img_path = f"assets/sga/{i + 1}.png"  # Generate image path dynamically

            # Create and store the button
            button = ToggleImageButton(
                self.root,
                sga_buttons_origin[0],
                sga_buttons_origin[1],
                img_path,
                self.lista_sga,
                img_path,
                x, y,
                button_width,
                button_height,
                i + 1
            )
            self.buttons_sga.append(button)

        epp_buttons_origin = [700, 600]
        button_width, button_height = 100, 140
        x_offset = 105  # Distance between buttons along x-axis

        for i in range(3):
            x = i * x_offset  # Calculate x position
            y = 0  # y is constant since all buttons are in the same row
            img_path = f"assets/epp/{i + 1}.png"  # Generate image path dynamically

            # Create and store the button
            button = ToggleImageButton(
                self.root,
                epp_buttons_origin[0],
                epp_buttons_origin[1],
                img_path,
                self.lista_epp,
                img_path,
                x, y,
                button_width,
                button_height,
                i + 1
            )
            self.buttons_epp.append(button)

    def update_form(self, datos):


        """
        Updates the form with data from a dictionary.
        :param datos: A dictionary containing the product data.
        """
        self.ficha.set(int(datos.get("FICHA", "0").split('°')[-1]))
        self.edicion.set(int(datos.get("EDICION", "0").split('°')[-1]))
        self.nombre_producto.set(datos.get("NOMBRE", ""))
        self.forma.set(datos.get("ESTADO", ""))
        self.responsable.set(datos.get("RESPONSABLE", "").replace("REVISADO POR: ", ""))

        # Set dates
        self.fecha_revision.set_date(datos.get("REVISION", "").replace("REVISION: ", ""))
        self.vigente.set_date(datos.get("VIGENTE", "").replace("VIGENTE: ", ""))

        # Set text areas
        self.text_riesgos.delete("1.0", "end")
        self.text_riesgos.insert("1.0", datos.get("RIESGOS", ""))

        self.text_manipulacion.delete("1.0", "end")
        self.text_manipulacion.insert("1.0", datos.get("MANIPULACION", ""))

        self.text_almacenamiento.delete("1.0", "end")
        self.text_almacenamiento.insert("1.0", datos.get("ALMACENAMIENTO", ""))

        self.text_eliminacion.delete("1.0", "end")
        self.text_eliminacion.insert("1.0", datos.get("ELIMINACION", ""))

        self.text_firstaid.delete("1.0", "end")
        self.text_firstaid.insert("1.0", datos.get("FIRSTAID", ""))

        self.text_derrame.delete("1.0", "end")
        self.text_derrame.insert("1.0", datos.get("DERRAME", ""))

        self.text_fuego.delete("1.0", "end")
        self.text_fuego.insert("1.0", datos.get("FUEGO", ""))

        for button in self.buttons_sga:
            button.toggle_button(force=False)
            for path in datos.get("SGA", ""):
                if path.endswith(f"/{button.id}.png"):

                    button.toggle_button(force=True)

        for button in self.buttons_epp:
            button.toggle_button(force=False)
            for path in datos.get("EPP", ""):
                if path.endswith(f"/{button.id}.png"):

                    button.toggle_button(force=True)


        FormIO.leer_datos(self)