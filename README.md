Crear un ejecutable .exe

Ejecuta:

pip install pyinstaller

Luego ejecuta:

pyinstaller --noconsole --onefile --add-data="assets:assets" --add-data="books_content:books_content" --add-data="quizzes:quizzes" --hidden-import tkinter main.py

Busca el ejecutable en la carpeta /dist
