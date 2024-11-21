import os
import tkinter as tk
from tkinter import messagebox, filedialog
from window.form import FormIO
from window.form.FormIO import *
from window.GUI_Builders import *
from pathlib import Path


class ExportWindow:
    # Class variable to track window state
    is_window_open = False

    def __init__(self, parent_form):
        # Check the class variable, not an instance variable
        if not ExportWindow.is_window_open:
            ExportWindow.is_window_open = True

            self.folder_path = parent_form.docx_output_path
            self.parent_form = parent_form

            filename = FormIO.leer_datos(self.parent_form)["NOMBRE"]
            if filename == "" or filename[0] == " ":
                print("ERROR: No filename selected.")
                messagebox.showwarning("Error",
                                       "El nombre del producto está vacío o es un nombre inválido.")
                ExportWindow.is_window_open = False  # Reset the flag if window creation fails
                return

            print("Opening export window...")
            self.root = tk.Toplevel(parent_form.root)
            self.root.title("Export Options")

            # Set up window close handler
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Rest of your window setup code...
            self.root.attributes('-topmost', True)
            self.root.resizable(False, False)

            window_width = 700
            window_height = 175
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)

            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

            # Create a label for folder selection
            self.folder_label = tk.Label(
                self.root, text="Carpeta de salida: ")
            self.folder_label.place(x=20, y=10)

            self.path_display = tk.Label(
                self.root, background="#AAAAAA", font=("Calibri", 11), text=self.folder_path)
            self.path_display.place(x=20, y=30)

            self.status_label = tk.Label(
                self.root, text=f"Nombre del Archivo: {leer_datos(self.parent_form)['NOMBRE']}.docx",
                font=("Calibri", 11))
            self.status_label.place(x=20, y=60)

            crear_boton(self.root, "Seleccionar Carpeta", self.select_folder, 20, 90, 150)
            crear_boton(self.root, "Exportar a DOCX (Word)", self.export_to_docx, 180, 90, 200)
            crear_boton(self.root, "Abrir en el Explorador", self.open_in_explorer, 390, 90, 200)

    def on_closing(self):
        """Handle window closing"""
        ExportWindow.is_window_open = False
        self.root.destroy()

    # Your existing methods remain the same
    def select_folder(self):
        top = tk.Toplevel()
        top.attributes('-topmost', True)
        top.focus_force()
        top.withdraw()
        try:
            folder_selected = filedialog.askdirectory(parent=top)
            if folder_selected:
                self.folder_path = folder_selected
                self.parent_form.docx_output_path = self.folder_path
                self.path_display.config(text=self.folder_path)
        finally:
            top.destroy()

    def open_in_explorer(self):
        os.startfile(self.folder_path)
        print(self.folder_path)

    def export_to_docx(self):
        output_folder = self.folder_path
        filename = leer_datos(self.parent_form)["NOMBRE"]
        filename = slugify(filename) + ".docx"
        if output_folder:
            print(filename, os.listdir(output_folder))
            if filename in os.listdir(output_folder):
                confirm_messagebox(
                    self.root,
                    "Advertencia de sobreescritura",
                    "Se ha encontrado un archivo con el mismo nombre en la carpeta de salida. ¿Está seguro que desea sobreescribir el archivo? Esta acción es permanente.",
                    confirm=lambda: exportar(self.parent_form, self.folder_path)
                )
            else:
                exportar(self.parent_form, self.folder_path)
                topmost_messagebox(
                    "Archivo exportado",
                    "El documento se exportó correctamente en la carpeta seleccionada."
                )
