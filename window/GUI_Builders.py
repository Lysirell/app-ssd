import tkinter as tk
from tkinter import messagebox
from xmlrpc.client import Boolean

from PIL import Image, ImageTk
from tkcalendar import DateEntry  # Ensure you have tkcalendar installed


# Limit the number of characters in a Text widget
def limitar_caracteres(text, limite):
    current_text = text.get("1.0", "end-1c")
    if len(current_text) > limite:
        text.delete("1.0", "end")
        text.insert("1.0", current_text[:limite])
        return "break"


# Limit the number of characters in an Entry widget
def limitar_caracteres_entry(entry, limite):
    current_text = entry.get()
    if len(current_text) > limite:
        entry.delete(0, "end")
        entry.insert(0, current_text[:limite])
        return "break"


# Create an Entry widget with a character limit
def crear_entry(parent, x_origin, y_origin, label_text, var, char_limit, lx, ly, width, ex, ey):
    tk.Label(parent, text=label_text).place(x=lx + x_origin, y=ly + y_origin)
    entry = tk.Entry(parent, textvariable=var, width=width)
    entry.place(x=ex + x_origin, y=ey + y_origin)
    entry.bind("<KeyPress>", lambda event: limitar_caracteres_entry(entry, char_limit)
    if event.keysym not in ('BackSpace', 'Delete') else None)
    entry.bind("<KeyRelease>", lambda event: limitar_caracteres_entry(entry, char_limit)
    if event.keysym not in ('BackSpace', 'Delete') else None)


# Create a DateEntry widget
def crear_date_entry(parent, x_origin, y_origin, label_text, lx, ly, dx, dy):
    tk.Label(parent, text=label_text).place(x=lx + x_origin, y=ly + y_origin)
    var = DateEntry(parent, width=10, date_pattern='yyyy-mm-dd')
    var.place(x=dx + x_origin, y=dy + y_origin)
    return var


# Create a button widget
def crear_boton(parent, text, command, x, y, width):
    button = tk.Button(parent, text=text, command=command)
    button.place(x=x, y=y, width=width)


# Create a checklist with multiple checkboxes
def crear_checklist(parent, x_origin, y_origin, label, descriptions, var_array, lx, ly, cy_start):
    tk.Label(parent, text=label).place(x=lx + x_origin, y=ly + y_origin)
    for i, desc in enumerate(descriptions):
        checkbox = tk.Checkbutton(parent, text=desc, variable=var_array[i])
        checkbox.place(x=lx + x_origin, y=cy_start + y_origin + (i * 17))


def crear_text_section(parent, x_origin, y_origin, label, char_limit, lx, ly, tx, ty, sx, sh, width=50, height=15):
    tk.Label(parent, text=label).place(x=lx + x_origin, y=ly + y_origin)

    text_widget = tk.Text(parent, width=width, height=height, font=("Calibri", 9), wrap="word")
    text_widget.bind("<KeyPress>", lambda event: limitar_caracteres(text_widget, char_limit)
    if event.keysym not in ('BackSpace', 'Delete') else None)
    text_widget.bind("<KeyRelease>", lambda event: limitar_caracteres(text_widget, char_limit)
    if event.keysym not in ('BackSpace', 'Delete') else None)

    # Scrollbar setup
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Place widgets
    text_widget.place(x=tx + x_origin, y=ty + y_origin)
    scrollbar.place(x=sx + x_origin, y=ty + y_origin, height=sh)

    # Return the text widget for later access
    return text_widget

#window/GUI_Builders.py

def topmost_messagebox(title, message):
    # Create a hidden window to act as the parent (to keep the messagebox on top)
    top = tk.Toplevel()
    top.withdraw()  # Hide the Toplevel window
    top.attributes('-topmost', True)  # Set it as topmost
    messagebox.showinfo(title, message, parent=top)
    top.destroy()


def confirm_messagebox(root, title, message, confirm=None, cancel=None):
    # Function to create a topmost confirmation box
    def on_confirm():
        top.destroy()
        confirm()

        topmost_messagebox(
            "Archivo exportado",
            "El documento se exportó correctamente en la carpeta seleccionada."
        )

    def on_cancel():
        top.destroy()
        cancel()

    # Create a top-level window for the messagebox
    top = tk.Toplevel(root)
    top.title(title)
    top.geometry("500x150")
    top.attributes("-topmost", True)  # Make it topmost

    # Message Label
    tk.Label(top, text=message, wraplength=400, font=("Calibri", 10)).pack(pady=20)

    # Buttons for Confirm and Cancel
    button_frame = tk.Frame(top)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Sobreescribir", command=on_confirm, width=10).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancelar", command=on_cancel, width=10).pack(side="right", padx=10)

class ToggleImageButton:
    def __init__(self, parent, x_origin, y_origin, image_path, array, toggle_target, x, y, width, height, id):
        """Initializes a toggle image button in the specified parent widget."""
        self.parent = parent
        self.array = array
        self.target_image_path = toggle_target
        self.is_toggled = False  # Track the button's toggle state
        self.id = id
        # Load and resize the original image
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height), Image.BILINEAR)

        # Create a normal and transparent version of the image
        self.normal_image_tk = ImageTk.PhotoImage(resized_image)

        transparent_image = resized_image.convert("RGBA")
        alpha = transparent_image.split()[3]  # Get the alpha channel
        transparent_image.putalpha(alpha.point(lambda p: p * 0.2))  # Set 50% transparency
        self.transparent_image_tk = ImageTk.PhotoImage(transparent_image)

        # Create the button with the transparent image initially (off state)
        self.button = tk.Button(
            self.parent,
            image=self.transparent_image_tk,
            command=self.toggle_button
        )
        self.button.image = self.transparent_image_tk  # Prevent garbage collection
        self.button.place(x=x_origin + x, y=y_origin + y, width=width, height=height)

    def toggle_pic(self, force=None):
        if force is None:
            """Add or remove the img path from the array of images that will be exported."""
            if self.target_image_path in self.array:
                self.array.remove(self.target_image_path)
            else:
                self.array.append(self.target_image_path)

            print(self.array)

        if force is not None:
            if force and self.target_image_path not in self.array:
                self.array.append(self.target_image_path)
            elif not force and self.target_image_path in self.array:
                self.array.remove(self.target_image_path)

    def toggle_button(self, force=None):
        """Toggle the button state and update its image."""
        if force is None:
            self.is_toggled = not self.is_toggled  # Toggle the state

        if force is not None:
            if force:
                self.is_toggled = True

            elif not force:
                self.is_toggled = False

        new_image = self.normal_image_tk if self.is_toggled else self.transparent_image_tk
        self.button.config(image=new_image)
        self.button.image = new_image  # Prevent garbage collection
        self.toggle_pic(force=force)