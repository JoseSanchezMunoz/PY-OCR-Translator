# --------- Módulos estándar de Python ---------
import tkinter as tk  # Módulo principal de Python para crear interfaces gráficas (GUI)

# ----------- Módulos internos del proyecto -----------
from views.gui_builder import GUIBuilder  # Clase que construye la interfaz gráfica (ventanas, botones, áreas de texto, imágenes, etc.)
from controllers.translator_controller import TranslatorController  # Controlador principal que maneja la lógica entre la interfaz y el procesamiento
import config.settings as settings  # Archivo de configuración general (parámetros reutilizables, constantes, etc.)

# -------- Punto de entrada del programa --------
if __name__ == "__main__":
    # Crear la ventana principal (root) con Tkinter
    root = tk.Tk()
    # Instanciar el constructor de la GUI con la ventana raíz
    gui = GUIBuilder(root)
    # Crear el controlador, pasándole la GUI y la raíz para manejar eventos, OCR, etc.
    ctrl = TranslatorController(root, gui)
    # Enlazar el controlador con la GUI para que los botones tengan efecto
    gui.set_controller(ctrl)
    # Asociar el cierre de la ventana a la lógica de detención del proceso de traducción (seguro y limpio)
    root.protocol("WM_DELETE_WINDOW", ctrl.stop_translation)
    # Iniciar el bucle principal de la interfaz (mantiene la ventana abierta y receptiva)
    root.mainloop()
