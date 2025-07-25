import tkinter as tk  # Tkinter: biblioteca estándar de Python para construir interfaces gráficas (GUI)
from tkinter import messagebox, scrolledtext  # messagebox: para mostrar alertas/emergentes. scrolledtext: cuadro de texto con barra de desplazamiento

from PIL import Image, ImageTk  # PIL (Pillow): manejo de imágenes. Image: para procesar imágenes, ImageTk: para mostrar imágenes en Tkinter

import cv2  # OpenCV: procesamiento de imágenes (transformaciones, conversiones de color, etc.)

class GUIBuilder:
    def __init__(self, root):
        self.root = root
        # Configuración básica
        root.title("Traductor OCR en Tiempo Real")
        root.configure(bg="#1e1e1e"); root.geometry("400x500")

        self.controller = None
        self._build()

    def set_controller(self, ctrl):
        self.controller = ctrl

    def _build(self):
        """
        Construye la interfaz gráfica de usuario.
        Incluye botones, etiquetas y cuadros de texto para mostrar resultados.
        """
        # Establecer tamaño de la interfaz
        self.root.geometry("400x500")
        # Label para Estado del OCR (activo / detenido). Inicialmente detenido
        self.status_label = tk.Label(self.root, text="🔴 OCR detenido", fg="red", bg="#1e1e1e", font=("Arial", 9, "bold"))
        self.status_label.pack(pady=(8, 0))

        # --- Área para los botones --- 
        # Frame para botones de control
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(fill=tk.X, pady=(10, 5))
        # Boton Activar
        self.activate_btn = tk.Button(frame, text="Activar", command=lambda:self.controller.start_area_selection(), bg="#4CAF50", fg="white")
        self.activate_btn.pack(side=tk.LEFT, padx=2)
        # Boton Pausar / Reanudar  (inicia deshabilitado)
        self.pause_btn = tk.Button(frame, text="Pausar", command=lambda:self.controller.toggle_pause(), bg="gold", fg="black", state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=2)
        # Boton Desactivar  (inicia deshabilitado)
        self.deactivate_btn = tk.Button(frame, text="Desactivar", command=lambda:self.controller.stop_translation(), bg="#f44336", fg="white", state=tk.DISABLED)
        self.deactivate_btn.pack(side=tk.LEFT, padx=2)
        # Boton Salir
        tk.Button(frame, text="Salir", command=lambda:self.controller.on_close(), bg="#555555", fg="white").pack(side=tk.RIGHT, padx=2)
        
        # --- Área de texto para mostrar el texto original (entrada del OCR) --- 
        tk.Label(self.root, text="Texto Original:", fg="white", bg="#1e1e1e").pack(padx=5)
        self.original_text = scrolledtext.ScrolledText(self.root, height=4, bg="#2e2e2e", fg="white", state=tk.DISABLED, wrap=tk.WORD)
        self.original_text.pack(padx=5, fill=tk.BOTH, expand=True)
        
        # --- Área de texto para mostrar traducción ---
        tk.Label(self.root, text="Texto Traducido:", fg="white", bg="#1e1e1e").pack(padx=5)
        self.translated_text = scrolledtext.ScrolledText(self.root, height=4, bg="#2e2e2e", fg="white", state=tk.DISABLED, wrap=tk.WORD)
        self.translated_text.pack(padx=5, fill=tk.BOTH, expand=True)

        # --- Sección visual de imágenes OCR ---
        tk.Label(self.root, text="Imágenes OCR (original vs preprocesada):", fg="white", bg="#1e1e1e").pack(pady=(10, 2))

        # Frame horizontal que contiene ambas imágenes
        self.image_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Labels para imágenes (se actualizarán dinámicamente)
        self.img_original_label = tk.Label(self.image_frame, bg="#1e1e1e")
        self.img_original_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        self.img_processed_label = tk.Label(self.image_frame, bg="#1e1e1e")
        self.img_processed_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)


    def update_button_states(self, activar=False, pausar=False, desactivar=False):
        """
        Activa o desactiva los botones de la interfaz según el estado actual.
        Se usa `.after(0, ...)` para asegurarse que se actualicen desde el hilo principal (GUI-safe).
        """
        self.root.after(0, lambda: [
            self.activate_btn.config(state=tk.NORMAL if activar else tk.DISABLED),
            self.pause_btn.config(state=tk.NORMAL if pausar else tk.DISABLED),
            self.deactivate_btn.config(state=tk.NORMAL if desactivar else tk.DISABLED)
        ])

    def show_images(self, img_original_cv, img_processed_cv):
        """
        Convierte y muestra las imágenes original y preprocesada en la GUI.
        """
        # Convertir de OpenCV (BGR o Gray) a PIL
        img_original = Image.fromarray(cv2.cvtColor(img_original_cv, cv2.COLOR_BGR2RGB))
        img_processed = Image.fromarray(img_processed_cv)  # ya está en escala de grises

        # Redimensionar (opcional) para ajustarlas a la GUI
        max_width = 180
        scale = lambda img: img.resize((max_width, int(img.height * max_width / img.width)), Image.LANCZOS)

        img_original = scale(img_original)
        img_processed = scale(img_processed)

        # Convertir a PhotoImage (Tkinter)
        self.tk_img_original = ImageTk.PhotoImage(img_original)
        self.tk_img_processed = ImageTk.PhotoImage(img_processed)

        # Mostrar en labels
        self.img_original_label.config(image=self.tk_img_original)
        self.img_processed_label.config(image=self.tk_img_processed)

    def update_texts(self, original, translated):
        """
        Actualiza el texto original y traducido en la GUI.
        """
        # ---- Texto original ---
        self.original_text.config(state=tk.NORMAL)
        self.original_text.delete(1.0, tk.END)
        self.original_text.insert(tk.END, original)
        self.original_text.config(state=tk.DISABLED)
        # ---- Texto traducido ---
        self.translated_text.config(state=tk.NORMAL)
        self.translated_text.delete(1.0, tk.END)
        self.translated_text.insert(tk.END, translated)
        self.translated_text.config(state=tk.DISABLED)

    def show_error(self, title, message):
        messagebox.showerror(title, message)
