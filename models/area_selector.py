# ----------- Interfaz gráfica (Tkinter) -----------
import tkinter as tk  # Módulo principal para construir la interfaz gráfica

class AreaSelector:
    """
    Permite al usuario seleccionar una región de pantalla
    arrastrando el mouse. Se usa para definir el área de captura OCR.
    """

    def __init__(self, master, callback):
        """
        Inicializa la ventana de selección de área.

        Parámetros:
        - master: ventana principal (Tk).
        - callback: función que recibirá las coordenadas (x, y, ancho, alto)
                    del área seleccionada al finalizar.
        """
        self.callback = callback  # Función que recibe las coordenadas finales
        self.start_x = self.start_y = 0  # Coordenadas donde el usuario hace clic inicialmente
        self.rect = None  # ID del rectángulo en el canvas

        # Se crea una ventana que cubre toda la pantalla para permitir seleccionar el área
        self.sel_win = tk.Toplevel()  # Nueva ventana encima del resto
        self.sel_win.attributes("-fullscreen", True)  # Se extiende a pantalla completa
        self.sel_win.attributes("-alpha", 0.3)  # Hace la ventana parcialmente transparente
        self.sel_win.configure(bg="blue")  # Color de fondo visible como filtro de selección
        self.sel_win.attributes("-topmost", True)  # Asegura que la ventana esté al frente

        # Se crea un canvas sobre esa ventana para dibujar el rectángulo de selección
        self.canvas = tk.Canvas(self.sel_win, cursor="cross", bg="blue")  # Cursor tipo cruz
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Ocupa todo el espacio de la ventana

        # Asigna funciones a los eventos del mouse sobre el canvas
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)  # Clic inicial
        self.canvas.bind("<B1-Motion>", self.on_move_press)        # Movimiento mientras se arrastra el mouse (sostenido)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)  # Al soltar el clic

    def on_button_press(self, event):
        """
        Inicia el dibujo del rectángulo cuando el usuario presiona el botón del mouse.

        Parámetros:
        - event: evento generado por el mouse al hacer clic por primera vez.
        """
        self.start_x, self.start_y = event.x, event.y  # Guarda posición inicial
        # Dibuja un rectángulo desde esa posición
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x, self.start_y,
            outline="red", width=2
        )

    def on_move_press(self, event):
        """
        Actualiza las coordenadas del rectángulo mientras el usuario arrastra el mouse.

        Parámetros:
        - event: evento generado por el movimiento del mouse (manteniendo)
        """
         # Se actualiza el tamaño del rectángulo según la posición actual
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        """
        Finaliza la selección del área y llama al callback con las coordenadas resultantes.

        Parámetros:
        - event: evento generado al soltar el clic.
        """
        # Calcula las coordenadas normalizadas (esquina superior izquierda y tamaño)
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)  # Esquina superior izquierda
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)  # Esquina inferior derecha
        w, h = x2 - x1, y2 - y1  # Calcula ancho y alto
        self.sel_win.destroy()  # Cierra la ventana de selección
        self.callback((x1, y1, w, h) if w > 0 and h > 0 else None) # Si el área tiene dimensiones válidas (>0), se pasa al callback