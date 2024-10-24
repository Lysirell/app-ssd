from tkinter import filedialog, messagebox
from window.form.FormIO import exportar  # Ensure this import matches your file structure
from window.GUI_Builders import *
from pathlib import Path

class ExportWindow:
    def __init__(self, parent_form):
        self.folder_path =  str(Path.home() / "Documents")
        self.parent_form = parent_form
        self.root = tk.Toplevel(parent_form.root)  # Create a new window
        self.root.title("Export Options")
        # Make the window always on top
        self.root.attributes('-topmost', True)

        # Make the window non-resizable
        self.root.resizable(False, False)  # (width, height)

        # Calculate center position
        window_width = 700
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set geometry: width x height + x_offset + y_offset
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create the label to display the folder path
        self.folder_label = tk.Label(self.root, text="Seleccionar la carpeta donde se guardará el archivo: ")
        self.folder_label.place(x=20, y=10)

        # Create a label to show the selected folder path
        self.path_display = tk.Label(self.root, background="#AAAAAA", font=("Calibri", 11), text=self.folder_path)
        self.path_display.place(x=20, y=30)

        crear_boton(self.root, "Seleccionar Carpeta", lambda: self.select_folder(), 20, 60, 150)
        crear_boton(self.root, "Exportar a .docx (Word)", lambda: self.export_to_docx(), 180, 60, 180)


    def select_folder(self):
        folder_selected = str(filedialog.askdirectory())  # Open folder selection dialog
        if folder_selected:
            self.folder_path = folder_selected  # Update the label with the chosen path
            self.path_display.config(text=self.folder_path)  # Update the label with the chosen path
    def export_to_docx(self):
        # Assuming the export function takes the output path and the instance of ProductoFormulario
        output_folder = self.folder_path
        if output_folder:
            exportar(self.parent_form, self.folder_path)  # Call your export function with the current form instance
            messagebox.showinfo("Success", "Document exported successfully!")
        else:
            messagebox.showwarning("Warning", "Please select an output folder.")