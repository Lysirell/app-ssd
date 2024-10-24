import tkinter as tk
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

    text_widget = tk.Text(parent, width=width, height=height, font=("Calibri", 9))
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
