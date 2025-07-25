# --------- Módulos estándar de Python ---------
import sys  # Información sobre el sistema y la plataforma (usado para verificar si es Windows)
import ctypes  # Permite ajustar configuración de bajo nivel en Windows, como el DPI Awareness

# --------- Librerías externas ---------
import pytesseract  # Motor OCR basado en Tesseract (extrae texto desde imágenes)

# Ruta al ejecutable de Tesseract OCR (necesario para Windows)
pytesseract.pytesseract.tesseract_cmd = r"D:/Programas/OCR/Tesseract-OCR/tesseract.exe"

# Ajustes de DPI Awareness para evitar escalado de pantalla que distorsione la captura
if sys.platform == "win32":  # Solo aplica para sistemas Windows
    try:
        # Para Windows 8.1 o superior: activa el modo de DPI awareness por aplicación
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            # Para versiones anteriores a 8.1: alternativa de DPI awareness global
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            # Si ambas fallan, se continúa sin aplicar correcciones
            pass