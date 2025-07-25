# ----------- Módulos estándar de Python -----------
import threading  # Permite la ejecución de tareas en segundo plano (OCR en hilo separado)
import time       # Se usa para pausas temporales entre iteraciones del OCR loop

# ----------- Librerías de terceros -----------
import numpy as np  # Utilizado para manejar imágenes como arrays (ImageGrab -> NumPy)
from PIL import ImageGrab  # Permite capturar regiones específicas de la pantalla (captura OCR)

# ----------- Interfaz gráfica (Tkinter) -----------
import tkinter as tk  # Módulo principal para construir la interfaz gráfica
from tkinter import messagebox  # Utilizado para mostrar cuadros de diálogo de advertencia o error


# ----------- Módulos internos del proyecto -----------
from models.ocr_engine import OCRProcessor  # Lógica para preprocesar imágenes y extraer texto usando OCR
from models.translation_engine import TranslatorEngine  # Lógica para traducir texto OCR (motor: Google Translate)
from models.area_selector import AreaSelector  # Herramienta para seleccionar el área de captura en pantalla

class TranslatorController:
    def __init__(self, root, gui):
        self.root = root  # Referencia a la ventana principal (Tk)
        self.gui = gui
        self.ocr = OCRProcessor()  # Instancia del procesador OCR personalizado
        self.translator = TranslatorEngine()  # Instancia del motor de traducción
        self.running = False # Bandera para controlar si el OCR está activo
        self.running_lock = threading.Lock()  # Lock para evitar condiciones de carrera
        self.paused = threading.Event()  # Evento para pausar/reanudar OCR sin detener el hilo
        self.paused.set()  # Inicialmente pausado (espera que el usuario active)
        # --- Estado de la aplicación ---
        self.capture_area = None  # Área seleccionada para hacer OCR (x, y, w, h)
        self.overlay_win = None  # Ventana de superposición durante la selección de área
        self.ocr_thread = None  # Referencia al hilo principal de OCR en segundo plano

    def is_running(self):
        """
        Devuelve True si el OCR está en ejecución.
        Se protege con un Lock para evitar lecturas inconsistentes en entorno multihilo.
        """
        with self.running_lock:
            return self.running

    def set_running(self, value):
        """
        Establece el estado de ejecución del OCR.
        Se protege con un Lock para garantizar escritura segura desde múltiples hilos.
        """
        with self.running_lock:
            self.running = value

    def start_area_selection(self):
        """
        Inicia la herramienta para seleccionar visualmente el área de captura OCR.
        Se ejecuta en un hilo separado para no bloquear la GUI.
        """
        threading.Thread(target=lambda: AreaSelector(self.root, self.set_capture_area), daemon=True).start()

    def set_capture_area(self, area):
        """
        Asigna el área seleccionada por el usuario y lanza el OCR si es válida.
        """
        if area:
            self.capture_area = area  # Guarda el área
            self.show_overlay(area)  # Muestra rectángulo visual
            self.start_translation()  # Inicia hilo de OCR
        else:
            messagebox.showwarning("Aviso", "Área no seleccionada correctamente.")

    def show_overlay(self, area):
        """
        Muestra un rectángulo rojo transparente sobre el área seleccionada.
        """
        x, y, w, h = area  # Coordenadas
        self.overlay_win = tk.Toplevel(self.root)
        self.overlay_win.overrideredirect(True)  # Sin bordes
        self.overlay_win.attributes("-topmost", True)  # Siempre encima
        self.overlay_win.attributes("-alpha", 0.3)  # Transparencia
        self.overlay_win.configure(bg="red")  # Rojo
        self.overlay_win.geometry(f"{w}x{h}+{x}+{y}") # Posicion según coordenadas seleccionadas

    def hide_overlay(self):
        """
        Oculta y destruye la superposición si está activa.
        """
        if self.overlay_win:
            self.overlay_win.destroy()
            self.overlay_win = None

    def start_translation(self):
        """
        Inicia el hilo que realiza OCR y traducción continuamente sobre el área seleccionada.
        """
        if not self.capture_area:
            messagebox.showerror("Error", "No se ha definido un área para capturar.")
            return
        if self.is_running():
            return # Ya está corriendo, no hace nada

        self.set_running(True)  # Marca como activo
        self.gui.status_label.config(text="🟢 OCR activo", fg="limegreen")
        self.gui.update_button_states(activar=False, pausar=True, desactivar=True)

        self.ocr_thread = threading.Thread(target=self.ocr_loop, daemon=True)
        self.ocr_thread.start()
        self.gui.pause_btn.config(state=tk.NORMAL)

    def stop_translation(self):
        """
        Detiene el proceso de OCR y borra la superposición visual.
        """
        self.set_running(False)
        self.gui.status_label.config(text="🔴 OCR detenido", fg="red")
        self.gui.update_button_states(activar=True, pausar=False, desactivar=False)
        self.hide_overlay()  # Elimina el rectángulo rojo
        self.gui.pause_btn.config(state=tk.DISABLED, text="Pausar")
        self.paused.set()   # Asegura que el hilo no quede bloqueado esperando `.wait()`

    def toggle_pause(self):
        """
        Pausa o reanuda la traducción dependiendo del estado actual.
        Cambia el texto y color de la etiqueta de estado y botón.
        """
        if self.paused.is_set():
            self.paused.clear()  # OCR queda en Pausa
            self.gui.status_label.config(text="⏸️ OCR en pausa", fg="orange")
            self.gui.pause_btn.config(text="Reanudar")
        else:
            self.paused.set()  # Reanuda OCR
            self.gui.status_label.config(text="🟢 OCR activo", fg="limegreen")
            self.gui.pause_btn.config(text="Pausar")

    def on_close(self):
        """
        Cierra la aplicación de forma segura, esperando si hay hilos activos.
        """
        self.set_running(False) # Señal para detener OCR loop
        if self.ocr_thread and self.ocr_thread.is_alive():
            self.root.after(100, self.check_thread_and_close)  # Espera a que termine el hilo
        else:
            self.root.destroy() # Cierra ventana principal

    def check_thread_and_close(self):
        """
        Verifica si el hilo de OCR sigue activo y espera hasta que termine para cerrar la app.
        """
        if self.ocr_thread and self.ocr_thread.is_alive():
            self.root.after(100, self.check_thread_and_close)
        else:
            self.root.destroy()

    def ocr_loop(self):
        """
        Ciclo principal que ejecuta OCR y traducción mientras esté activo.
        Captura pantalla, procesa imagen, extrae texto y lo traduce.
        """
        time.sleep(2) # Pequeña espera antes de comenzar
        last_text = ""  # Guarda el último texto para evitar repeticiones innecesarias

        while self.is_running():
            self.paused.wait()  # Se detiene aquí si el OCR está en pausa
            try:
                # Captura la imagen del área seleccionada
                x, y, w, h = self.capture_area
                img = np.array(ImageGrab.grab((x, y, x + w, y + h)))

                # Procesamiento y extracción de texto
                processed = self.ocr.preprocess_image(img)

                # Encola la actualización visual de las imágenes (original y transformada) en el hilo principal de Tkinter
                self.root.after(0, self.gui.show_images, img, processed)

                text = self.ocr.extract_text(processed)
                text = self.ocr.corregir_errores_comunes(text)
                text = self.ocr.corregir_letra_i(text)

                # Si está vacío, se marca explícitamente
                if not text:
                    text = "<VACÍO>"
                # Solo se traduce si el texto cambió desde la última iteración (Evitamos envios repetidos)
                if text != last_text:
                    last_text = text
                    translated = self.translator.translate(text)
                    self.root.after(0, self.gui.update_texts, text, translated)
            except Exception as e:
                # En caso de error, se muestra el tipo de excepción
                self.root.after(0, self.gui.update_texts, "<ERROR>", f"{type(e).__name__}: {e}")

            time.sleep(0.5) # Espera entre ciclos para evitar sobrecarga de CPU