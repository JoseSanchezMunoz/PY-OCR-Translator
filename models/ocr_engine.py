# --------- Módulos estándar de Python ---------
import re  # Expresiones regulares (usado para corregir errores comunes del OCR)

# --------- Librerías externas ---------
import cv2  # OpenCV: procesamiento de imágenes (transformaciones, conversiones de color, etc.)
import pytesseract  # Motor OCR basado en Tesseract (extrae texto desde imágenes)

class OCRProcessor:
    """
    Clase que maneja todo lo relacionado al reconocimiento de texto (OCR)
    desde una imagen capturada de pantalla.
    """

    def __init__(self):
        """
        Inicializa el motor de OCR con una configuración por defecto.
        - oem 3: modo OCR automático.
        - psm 6: asume un bloque uniforme de texto.
        - l eng: idioma en inglés.
        """
        self.config = r'--oem 3 --psm 6 -l eng'

    def preprocess_image(self, img):
        """
        Aplica una serie de transformaciones a la imagen capturada
        para mejorar la precisión del OCR (mejora brillo, contraste y resolución).

        Parámetros:
        - img: imagen original en formato BGR (color).

        Retorna:
        - Imagen preprocesada en escala de grises, ampliada.
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convierte imagen de BGR a HSV
        h, s, v = cv2.split(hsv)  # Separa los canales Hue, Saturation y Value
        s = cv2.add(s, 80)  # Aumenta la saturación (mejora contraste)
        v = cv2.add(v, 80)  # Aumenta el brillo (mejora visibilidad)
        enhanced = cv2.merge((h, s, v))  # Vuelve a unir los canales
        bgr = cv2.cvtColor(enhanced, cv2.COLOR_HSV2BGR)  # Vuelve a formato BGR
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)  # Convierte a escala de grises
        resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)  # Duplica tamaño para mayor claridad
        return resized

    def extract_text(self, image):
        """
        Ejecuta el motor OCR sobre una imagen para extraer el texto.

        Parámetros:
        - image: imagen preprocesada

        Retorna:
        - Texto extraído sin saltos de línea.
        """
        return pytesseract.image_to_string(image, config=self.config).strip().replace('\n', ' ')

    def corregir_errores_comunes(self, texto):
        """
        Corrige errores comunes que comete el OCR al reconocer letras similares,
        como confundir la "I" con "l".

        Parámetros:
        - texto: cadena de texto extraída por OCR.

        Retorna:
        - Texto con algunas correcciones automáticas aplicadas.
        """
        reemplazos = {
            r"\bl\b": "I",
            r"\bl'm\b": "I'm",
            r"\bl've\b": "I've",
            r"\bl'd\b": "I'd",
            r"\bl'll\b": "I'll",
            r"\bl don't\b": "I don't"
        }
        for k, v in reemplazos.items():
            texto = re.sub(k, v, texto)
        return texto

    def corregir_letra_i(self, texto):
        """
        Reemplaza palabras que probablemente representan mal la letra "I" (como "|" o "l").

        Parámetros:
        - texto: texto ya corregido o extraído por OCR.

        Retorna:
        - Texto con sustituciones específicas para mejorar la lectura.
        """
        palabras = texto.split()  # Divide el texto en palabras
        nuevas = []
        for palabra in palabras:
            if palabra in {'|', 'l'}:
                nuevas.append('I')  # Si es solo "l" o "|", reemplaza directamente
            elif re.fullmatch(r'[|l][.,;:!?]?', palabra):  # Coincide con variantes como "l.", "|!"
                nuevas.append(re.sub(r'[|l]', 'I', palabra))  # Reemplaza carácter por "I"
            else:
                nuevas.append(palabra)  # Si no, deja la palabra tal cual
        return ' '.join(nuevas)  # Une todo nuevamente