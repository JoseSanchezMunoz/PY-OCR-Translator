# --------- Librerías externas ---------
from googletrans import Translator  # Traducción automática utilizando Google Translate

class TranslatorEngine:
    """
    Clase encargada de traducir texto usando la API de Google Translate.
    """

    def __init__(self):
        """
        Inicializa una instancia del traductor de Google usando la librería `googletrans`.
        """
        self.translator = Translator()  # Crea un traductor que puede detectar idioma y traducir

    def translate(self, text, src='auto', dest='es'):
        """
        Traduce el texto especificado desde un idioma fuente a uno destino.

        Parámetros:
        - text: texto que se desea traducir.
        - src: idioma de origen. Por defecto es 'auto' para detección automática.
        - dest: idioma destino. Por defecto es 'es' (español).

        Retorna:
        - Texto traducido si la solicitud fue exitosa.
        - Mensaje de error personalizado si ocurre una excepción.
        """
        try:
            # Realiza la traducción usando Google Translate
            return self.translator.translate(text, src=src, dest=dest).text
        except Exception as e:
            # Si ocurre un error (como fallo de conexión), se devuelve un mensaje de error
            return f"<ERROR DE TRADUCCIÓN: {e}>"