# src/config.py

import os
import sys

APP_NAME = "AtlasRead"
DB_NAME = "atlasread.db" # Nombre del archivo de la base de datos

# Configuraciones de velocidad de lectura (palabras por minuto)
# Estas son estimaciones y pueden ajustarse
WPM_EXPECTED = {
    6: (30, 60),    # Niños de 6 años
    7: (40, 70),
    8: (50, 80),
    9: (60, 90),
    10: (70, 100),
    11: (80, 120),
    12: (90, 130),
    13: (100, 140),
    14: (110, 150),
    15: (120, 160),
    # Edades mayores (promedio adulto)
    16: (150, 250),
    17: (150, 250),
    18: (150, 250),
    # Para cualquier edad por encima de 18, usar el rango de 18
    'default': (150, 250)
}

# --- FUNCIÓN CENTRAL PARA DETERMINAR LA RUTA BASE ---
def get_base_path():
    """
    Determina la ruta base de la aplicación.
    Si se ejecuta como un ejecutable de PyInstaller, usa sys._MEIPASS o el directorio del ejecutable.
    Si se ejecuta como script, usa la raíz del proyecto.
    """
    if getattr(sys, 'frozen', False): # True si se ejecuta como ejecutable de PyInstaller
        # sys._MEIPASS es el directorio temporal donde PyInstaller extrae los datos.
        # Si no está disponible (ej. modo onefile y PyInstaller no lo usa así),
        # usamos el directorio del ejecutable (donde está AtlasRead.exe/AtlasRead).
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # En modo desarrollo (ejecutando con `python src/main.py`):
        # __file__ es src/config.py
        # os.path.dirname(__file__) es src/
        # os.path.dirname(os.path.dirname(__file__)) es la raíz del proyecto (Atlasread/)
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas a los recursos, construidas usando la función get_base_path
# Estas rutas ya son absolutas y válidas tanto en desarrollo como en el ejecutable.
DATABASE_PATH = os.path.join(get_base_path(), DB_NAME)
BOOKS_DIRECTORY = os.path.join(get_base_path(), "src", "books_content") # Los libros están en src/books_content
QUIZZES_DIRECTORY = os.path.join(get_base_path(), "src", "quizzes") # Los quizzes están en src/quizzes

# (Opcional, para depuración)
# print(f"DEBUG - Ruta base de la aplicación: {get_base_path()}")
# print(f"DEBUG - Ruta de la base de datos: {DATABASE_PATH}")
# print(f"DEBUG - Ruta del directorio de libros: {BOOKS_DIRECTORY}")
# print(f"DEBUG - Ruta del directorio de cuestionarios: {QUIZZES_DIRECTORY}")