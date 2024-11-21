import os
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar, Listbox

from window.DatabaseIO import DatabaseIO
from window.form import FormIO  # Assuming this is your FormIO import
from window.form.FormIO import leer_datos, slugify


class FileBrowser:
    def __init__(self, parent, x=0, y=0, width=400, height=300):
        self.parent = parent  # Store parent for later reference
        self.file_path = None  # Track the currently selected file path

        # Frame to hold all widgets
        self.frame = tk.Frame(parent.root, bd=2, relief='sunken')
        self.frame.place(x=x, y=y, width=width, height=height)

        # Button to change directory (folder selection)
        self.change_folder_button = tk.Button(
            self.frame, text="Cambiar Carpeta de Origen", command=self.choose_folder
        )
        self.change_folder_button.place(x=10, y=10, width=width - 20, height=30)

        # Current path label
        self.path_label = tk.Label(self.frame, text="Mostrando archivos de la carpeta actual: No se ha elegido ninguna carpeta.", anchor='w')
        self.path_label.place(x=10, y=50, width=width - 20, height=20)

        # File list (Listbox) with scrollbar
        self.file_list = Listbox(self.frame, selectmode=tk.SINGLE)
        self.scrollbar = Scrollbar(self.frame, orient=tk.VERTICAL, command=self.file_list.yview)
        self.file_list.config(yscrollcommand=self.scrollbar.set)

        self.file_list.place(x=10, y=80, width=width - 40, height=height - 130)
        self.scrollbar.place(x=width - 30, y=80, width=20, height=height - 130)

        # Navigation buttons
        self.refresh_button = tk.Button(self.frame, text="Refresh", command=self.refresh)
        self.import_button = tk.Button(self.frame, text="Importar Archivo", command=self.import_file)

        self.refresh_button.place(x=10, y=height - 40, width=60, height=30)
        self.import_button.place(x=80, y=height - 40, width=120, height=30)

        # Sobreescribir button
        self.overwrite_button = tk.Button(
            self.frame, text="Exportar a STD", command=self.save_std
        )
        self.overwrite_button.place(x=210, y=height - 40, width=110, height=30)

        # New Open in Explorer button
        self.explorer_button = tk.Button(
            self.frame, text="Abrir carpeta en el Explorador", command=self.open_in_explorer
        )
        self.explorer_button.place(x=330, y=height - 40, width=200, height=30)

        # Bind double-click event to the file list
        self.file_list.bind("<Double-Button-1>", self.on_file_double_click)

        # Store the current directory
        self.current_path = "No se ha elegido una carpeta"


    def open_in_explorer(self):
        """Opens the current directory in the system's file explorer"""
        os.startfile(self.current_path)
        print(self.current_path)

    # Rest of the methods remain unchanged
    def load_directory(self, path):
        """Loads the .json files from the given directory into the listbox."""
        try:
            self.file_list.delete(0, tk.END)
            self.path_label.config(text=f"Mostrando archivos estándar (STD) -> {path}")

            # List only .json files
            entries = sorted(
                entry for entry in os.listdir(path) if entry.endswith('.json')
            )
            for entry in entries:
                self.file_list.insert(tk.END, entry)

            self.current_path = path
            self.parent.std_folder = self.current_path
        except PermissionError:
            messagebox.showerror("Error", "Permission denied.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Directory not found.")

    def choose_folder(self):
        """Opens a dialog to select a new folder and loads it."""
        # Create a temporary toplevel window to force the dialog to be topmost
        top = tk.Toplevel()
        top.attributes('-topmost', True)  # Make it topmost
        top.focus_force()  # Force focus
        # Hide the temporary window
        top.withdraw()
        try:
            folder_path = filedialog.askdirectory(parent=top)
            if folder_path:
                self.load_directory(folder_path)
        finally:
            # Destroy the temporary window
            top.destroy()

    def refresh(self):
        """Refreshes the current directory listing."""
        self.load_directory(self.current_path)

    def import_file(self):
        """Imports the selected file by reusing the double-click logic."""
        self.on_file_double_click(None)  # Reuse the double-click logic
        self.refresh()
    def on_file_double_click(self, event):
        """Handles double-clicking on a file to load its data."""
        selection = self.file_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No file selected.")
            return

        selected = self.file_list.get(selection[0])
        self.file_path = os.path.join(self.current_path, selected)
        response = messagebox.askyesno("Confirmar carga del archivo",
                                       "Está a punto de importar este archivo. Los datos no guardados serán eliminados. ¿Desea proceder y cargar el archivo?")
        if response:
            self.load_data()  # Call the load_data function

    def load_data(self):
        """Loads data from the selected file and updates the parent form."""
        if not self.file_path:
            messagebox.showwarning("Warning", "No file selected.")
            return

        # Load data using FormIO.deserialize
        datos = FormIO.deserialize(self.file_path)
        if datos:
            # Call the parent form's update method with the loaded data
            self.parent.update_form(datos)

    def save_std(self):
        """Displays a confirmation dialog for overwriting the selected file."""
        product_name = leer_datos(self.parent)["NOMBRE"]
        filename = slugify(product_name)
        if filename.startswith(" ") or filename == "":
            messagebox.showwarning("ERROR", "El nombre del producto está vacío o contiene carácteres inválidos.")
            return

        # Ask for confirmation
        if filename + "-STD.json" in os.listdir(self.current_path):

            response = messagebox.askyesno(
                f"Advertencia de sobreescritura",
                f"Está seguro de que desea continuar? Se está por sobreescribir el archivo con el mismo nombre: {filename}"
            )
            if response:
                FormIO.serialize(self.current_path, leer_datos(self.parent))
        else:
            FormIO.serialize(self.current_path, leer_datos(self.parent))
            messagebox.showinfo("Archivo guardado:", f"Salida: {self.current_path}")

        DatabaseIO.add_product(product_name, filename + "-STD.json")

        self.refresh()