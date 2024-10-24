from tkinter import ttk

import tkcalendar

from window.form import FormIO
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

    def init_variables(self):
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
            "Guantes de Seguridad", "Mascara respiratoria", "Gafas de Seguridad"
        ]
        self.sga_vars = [tk.IntVar(self.root) for _ in self.sga_descripciones]
        self.epp_vars = [tk.IntVar(self.root) for _ in self.epp_descripciones]

        self.lista_sga = [tk.IntVar(self.root) for _ in self.sga_descripciones]
        self.lista_epp = [tk.IntVar(self.root) for _ in self.epp_descripciones]

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
        crear_boton(self.root, "Importar Datos", lambda: FormIO.cargar_datos(self), 1030, 20, 150)
        crear_boton(self.root, "Guardar Datos", lambda: FormIO.guardar_datos(self), 1200, 20, 150)
        crear_boton(self.root, "Exportar Formulario", self.open_export_window, 1200, 50, 150)



    def open_export_window(self):
        print("Opening export window...")
        export_window = ExportWindow(self)

    def crear_secciones(self):
        """Creates all sections of the form (Pictograms, EPP, Text fields)."""
        # Separador
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', pady=95)

        # Checklists
        crear_checklist(self.root, 700, 110, "Pictogramas SGA (Código Numérico)", self.sga_descripciones, self.lista_sga, 0,
                              0,  50)
        crear_checklist(self.root, 700, 320, "EPP Obligatorios",
                              self.epp_descripciones, self.lista_epp, 0, 0, 20)

        # Secciones de texto
        self.text_riesgos = crear_text_section(self.root, 10, 100, "Riesgos del Producto", 600, 0, 0, 20, 20, 0, 210)
        self.text_manipulacion = crear_text_section(self.root, 350, 100, "Consignas de Manipulación Segura", 600, 0, 0, 20,
                                 20, 0, 210)

        self.text_almacenamiento = crear_text_section(self.root, 10, 335, "Consignas de Almacenamiento Seguro", 600, 0, 0, 20,
                                 20, 0, 210)

        self.text_eliminacion = crear_text_section(self.root, 350, 335, "Consignas de Eliminación o Desecho", 600, 0, 0, 20,
                                 20, 0, 210)

        self.text_firstaid = crear_text_section(self.root, 10, 570, "Primeros Auxilios", 600, 0, 0,
                                                   20,
                                                   20, 0, 150, width=107, height=12)

        self.text_derrame = crear_text_section(self.root, 10, 765, "En caso de Derrame", 600, 0, 0,
                                                   20,
                                                   20, 0, 210)

        self.text_fuego = crear_text_section(self.root, 350, 765, "En caso de Fuego", 600, 0, 0,
                                                   20,
                                                   20, 0, 210)