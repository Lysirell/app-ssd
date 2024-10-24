"""
----------------------------------------------------------------------------------------------
    Este script crea una interfaz gráfica de usuario (GUI) para el diseño de fichas
    de puesto de trabajo para productos químicos, utilizando la librería `tkinter`.
    La clase principal `ProductoFormulario` se encarga de construir el formulario,
    que permite ingresar datos esenciales como el número de hoja, edición, fechas y
    consignas de seguridad.

    La interfaz incluye validaciones para asegurar que los datos ingresados
    sean correctos, y botones de acción para importar, guardar y exportar
    información. Además, se implementa una función para limitar el número
    de caracteres en los campos de texto.

    Se recomienda utilizar PyCharm en lugar de VSCode para el desarrollo
    de este proyecto, debido a sus ventajas en autocompletado, detección de
    errores y un depurador más avanzado, lo que facilita la gestión de
    proyectos complejos.

    Al ejecutar el script, se inicializa la ventana principal y se instancia
    el formulario, el cual permanece activo hasta que se cierre la ventana.
----------------------------------------------------------------------------------------------
"""

from window.form.Form import *

if __name__ == "__main__":
    root = tk.Tk()  # Inicializa la ventana principal
    app = ProductoFormulario(root)  # Crea una instancia del formulario
    root.mainloop()  # Inicia el bucle de eventos de la GUI


