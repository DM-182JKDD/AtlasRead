# src/config.py

APP_NAME = "AtlasRead"
DB_NAME = "atlasread.db"

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

# Ruta a los libros de muestra
BOOKS_DIRECTORY = "src/books_content"

# Ruta a los cuestionarios
QUIZZES_DIRECTORY = "src/quizzes" # Nueva línea