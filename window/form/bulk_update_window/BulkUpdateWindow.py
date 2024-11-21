import os
from tkinter import filedialog
from window.form import FormIO
from window.form.FormIO import *
from window.GUI_Builders import *
from pathlib import Path
import json
from window.DatabaseIO import DatabaseIO


class BulkUpdateWindow:
    # Class variable to track window state
    is_window_open = False

    def __init__(self, parent_form):
        # Check the class variable, not an instance variable

        if not BulkUpdateWindow.is_window_open:
            BulkUpdateWindow.is_window_open = True

            self.docx_folder_path = parent_form.docx_output_path
            self.std_folder_path = parent_form.std_folder
            self.parent_form = parent_form

            # todo: Hacer campos de texto que tomen estos datos de abajo, y los actualicen para todos los archivos .std
            #  y luego hacer una función que actualice la base de datos leyendo todos los nuevos archivos STD.
            #  También hacer una que transforme todos los STD en .DOCX

            self.new_responsable = tk.StringVar(self.parent_form.root)
            self.new_edicion = tk.IntVar(self.parent_form.root)



            print("Opening export window...")
            self.root = tk.Toplevel(parent_form.root)
            self.root.title("Bulk Update & Export")

            # Set up window close handler
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Rest of your window setup code...
            self.root.attributes('-topmost', True)
            self.root.resizable(False, False)

            window_width = 800
            window_height = 400
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)

            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

            # Create a label for folder selection
            self.folder_label = tk.Label(
                self.root, text="Carpeta de origen STD: ")
            self.folder_label.place(x=20, y=10)

            display = "No hay carpeta seleccionada."
            if self.std_folder_path != "No hay carpeta seleccionada.":
                if len(self.std_folder_path) > 45:
                    display = self.std_folder_path[:20] + " ... " + self.std_folder_path[-20:]
                else:
                    display = self.std_folder_path


            self.path_display = tk.Label(
                self.root, background="#AAAAAA", font=("Calibri", 11), text=display)
            self.path_display.place(x=20, y=40)

            # Create a label for folder selection
            self.folder_label = tk.Label(
                self.root, text="Salida de archivos DOCX: ")
            self.folder_label.place(x=20, y=70)

            display = "No hay carpeta seleccionada."
            if self.docx_folder_path != "No hay carpeta seleccionada.":
                if len(self.docx_folder_path) > 45:
                    display = self.docx_folder_path[:20] + " ... " + self.docx_folder_path[-20:]
                else:
                    display = self.docx_folder_path

            self.docx_path_display = tk.Label(
                self.root, background="#AAAAAA", font=("Calibri", 11), text=display)
            self.docx_path_display.place(x=20, y=100)

            crear_boton(self.root, "Actualizar todos los STD", self.update_database, 20, 370, 150)
            crear_boton(self.root, "Exportar todos los STD a DOCX", self.export_to_docx, 180, 370, 200)
            crear_boton(self.root, "Seleccionar carpeta de salida para DOCX", self.select_folder, 390, 370, 240)

            self.create_form()

    def create_form(self):
        crear_entry(self.root, 350, 10, "Responsable de Revisión:", self.new_responsable, 55, 0, 0, 60, 0, 20)
        crear_entry(self.root, 350, 60, "Edición N°", self.new_edicion, 4, 0, 0, 13, 0, 20)
        self.new_revision = crear_date_entry(self.root, 450, 60, "Revisión:", 0, 0, 0, 20)
        self.new_vigente = crear_date_entry(self.root, 550, 60, "Vigente:", 0, 0, 0, 20)

    def select_folder(self):
        top = tk.Toplevel()
        top.attributes('-topmost', True)
        top.focus_force()
        top.withdraw()
        try:
            folder_selected = filedialog.askdirectory(parent=top)
            if folder_selected:
                self.parent_form.docx_output_path = folder_selected
                self.docx_folder_path = folder_selected
                self.docx_path_display.config(text=folder_selected)
        finally:
            print(folder_selected)
    def on_closing(self):
        """Handle window closing"""
        BulkUpdateWindow.is_window_open = False
        self.root.destroy()

    def export_to_docx(self):
        output_path = self.docx_folder_path
        for std in os.listdir(self.std_folder_path):
            if std.endswith("-STD.json"):
                try:
                    data = FormIO.deserialize(Path(self.std_folder_path, std))
                    print(data)
                    doc = Document("template.docx")

                    # Replace the placeholder with the name from the form data
                    SheetWriter.fill_form(doc, data)

                    # Define the output paths
                    filename = slugify(data["NOMBRE"])
                    word_file_path = f"{output_path}/{filename}.docx"

                    # Save the Word document
                    doc.save(word_file_path)


                    print("Document saved:", word_file_path)
                except Exception as e:
                    print(e)


    def update_database(self):
        for filename in os.listdir(self.std_folder_path):
            print(filename)
            if filename.endswith("-STD.json"):
                try:
                    with open(f"{self.std_folder_path}/{filename}", "r+") as json_file:
                        data = json.load(json_file)

                        DatabaseIO.add_product(data["NOMBRE"], filename)

                except FileNotFoundError:
                    print(f"Error: File '{filename}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

                data["RESPONSABLE"] = str("RESPONSABLE: " + str(self.new_responsable.get()))
                data["EDICION"] = str("EDICION N°" + str(self.new_edicion.get()))
                data["REVISION"] = str("REVISION: " + str(self.new_revision.get_date()))
                data["VIGENTE"] = str("VIGENTE: " + str(self.new_vigente.get_date()))

            with open(Path(self.std_folder_path, filename), "w+") as json_file:
                json.dump(data, json_file, indent=4)

        for product_name, filenames in DatabaseIO.product_files.items():
            if len(filenames) > 1:
                print(f"Product '{product_name}' has repeated filenames: {filenames}")