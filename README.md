# PY-OCR-Translator



Una herramienta para capturar texto desde imágenes a tiempo real, a fin de traducirlas a tu idioma de preferencia.



Nota: De momento solo disponible para versión Ingles -> Español



\# 🧠 Traductor OCR (Interfaz Gráfica)



Este proyecto es una \*\*aplicación de escritorio en Python\*\* que permite \*\*capturar texto de la pantalla mediante OCR y traducirlo automáticamente\*\* a otro idioma usando la API de Google Translate. Dispone de una \*\*interfaz gráfica amigable\*\* construida con `Tkinter`, lo que facilita su uso incluso a usuarios sin conocimientos técnicos.



---



\## 🚀 Características principales



\- Captura automática del texto visible en pantalla (OCR).

\- Traducción inmediata del contenido a múltiples idiomas.

\- Interfaz visual simple e intuitiva.

\- Detección automática de idioma fuente (`auto`).

\- Modo traducción continua o puntual.

\- Diseño modular y mantenible.



---



\## 🛠️ Tecnologías y librerías utilizadas



\- \*\*Python 3.12.7\*\*

\- `tkinter` – para construir la GUI.

\- `pytesseract` – OCR para extraer texto desde capturas.

\- `opencv-python` – procesamiento de imágenes.

\- `googletrans` – traducción automática usando Google Translate.

\- `pyautogui`, `mouseinfo` – captura de pantalla y coordenadas del mouse.

\- `numpy`, `Pillow`, entre otras.



---



\## 📁 Estructura del proyecto



traductor\_ocr\_gui/

│

├── main.py                          # Punto de entrada del programa

├── controllers/

│   └── translator\_controller.py     # Lógica entre interfaz y procesamiento

│

├── models/

│   └── translator\_engine.py         # Lógica de traducción (Google Translate)

│

├── services/

│   └── ocr\_service.py               # Lógica OCR usando Tesseract

│

├── views/

│   └── gui\_builder.py               # Construcción de la interfaz Tkinter

│

├── config/

│   └── settings.py                  # Parámetros reutilizables y configuraciones

│

├── requirements.txt                 # Dependencias necesarias

└── README.md                        # Este archivo



---



\## 📦 Instalación y ejecución



\### 1. Clona el repositorio



git clone https://github.com/JoseSanchezMunoz/PY-OCR-Translator.git

cd PY-OCR-Translator



\### 2. Crea un entorno virtual (recomendado)



python -m venv venv



Actívalo:



\- En Windows:

&nbsp; venv\\Scripts\\activate



\- En Linux/macOS:

&nbsp; source venv/bin/activate



\### 3. Instala las dependencias



pip install -r requirements.txt



\### 4. Instala Tesseract OCR



Este proyecto requiere que tengas instalado el motor Tesseract en tu sistema:



\- En Windows:  

&nbsp; Descargar ejecutable oficial: https://github.com/tesseract-ocr/tesseract/wiki



\- En Linux:

&nbsp; sudo apt install tesseract-ocr



> Asegúrate de que `tesseract` esté en el PATH del sistema para que funcione `pytesseract`.



Edita la siguiente línea del archivo ocr_engine.py si es necesario:

> pytesseract.pytesseract.tesseract_cmd = r"D:/Programas/OCR/Tesseract-OCR/tesseract.exe"

---



\## 🧪 Cómo usarlo



1\. Ejecuta el programa:



python main.py



2\. Usa los botones de la interfaz para:

&nbsp;  - Iniciar o detener la traducción automática.

&nbsp;  - Pausar o Reanudar la traducción

&nbsp;  - Traducir un área capturada (de manera continua y a tiempo real)

&nbsp;  - Ver el texto original y traducido.



---



\## 📄 Licencia



Este proyecto puede ser reutilizado libremente siempre que se brinde el crédito correspondiente.



---



\## 👨‍💻 Autor



\*\*José Sánchez Muñoz\*\*  

Ingeniero de Sistemas  

🔗 GitHub: https://github.com/JoseSanchezMunoz



> Si te resulta útil este proyecto, ¡no dudes en darle una ⭐ en GitHub!



