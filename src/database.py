import sqlite3
import os
# import sys # <--- ¡ELIMINAR O COMENTAR ESTA LÍNEA! Ya no es necesaria aquí.

# Importar las rutas ya resueltas desde config.py
from src.config import DB_NAME, BOOKS_DIRECTORY, DATABASE_PATH


class DatabaseManager:
    def __init__(self):
        # Ahora, self.db_path simplemente usa la ruta ya resuelta de config.py
        self.db_path = DATABASE_PATH

        print(f"Conectado a la base de datos: {self.db_path}")
        self._create_tables()
        self._insert_sample_books()  # Esta función crea/inserta libros si no existen

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                min_age INTEGER NOT NULL,
                max_age INTEGER NOT NULL,
                content_path TEXT UNIQUE NOT NULL,
                word_count INTEGER NOT NULL DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reading_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration_seconds INTEGER,
                wpm REAL,
                age_appropriateness_score REAL,
                performance_rating TEXT,
                quiz_score REAL DEFAULT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        """)
        conn.commit()
        conn.close()
        print("Tablas verificadas/creadas exitosamente.")

    def _insert_sample_books(self):
        # Asegúrate de que los archivos de contenido de los libros existen ANTES de intentar insertarlos.
        # Esto es especialmente importante para que el _get_word_count_from_file no falle.
        books_to_insert = [
            {"title": "El Patito Feo", "author": "Hans Christian Andersen", "min_age": 6, "max_age": 8,
             "content_filename": "patito_feo.txt"},
            {"title": "Caperucita Roja", "author": "Hermanos Grimm", "min_age": 6, "max_age": 8,
             "content_filename": "caperucita_roja.txt"},
            {"title": "El Gato con Botas", "author": "Charles Perrault", "min_age": 7, "max_age": 9,
             "content_filename": "gato_botas.txt"},
            {"title": "Alicia en el País de las Maravillas", "author": "Lewis Carroll", "min_age": 9, "max_age": 12,
             "content_filename": "alicia_maravillas.txt"},
            {"title": "El Principito", "author": "Antoine de Saint-Exupéry", "min_age": 10, "max_age": 14,
             "content_filename": "principito.txt"},
            {"title": "Veinte Mil Leguas de Viaje Submarino", "author": "Julio Verne", "min_age": 12, "max_age": 99,
             "content_filename": "veinte_mil_leguas.txt"},
            {"title": "Don Quijote de la Mancha (Adaptación)", "author": "Miguel de Cervantes", "min_age": 14,
             "max_age": 99, "content_filename": "don_quijote.txt"},
            {"title": "Orgullo y Prejuicio", "author": "Jane Austen", "min_age": 16, "max_age": 99,
             "content_filename": "orgullo_prejuicio.txt"},
            {"title": "Ciencia Maya", "author": "Fundación Kinal", "min_age": 14, "max_age": 70,
             "content_filename": "ciencia_maya.txt"},
            {"title": "El Cambio Climático", "author": "Fundación Kinal", "min_age": 13, "max_age": 80,
             "content_filename": "el_cambio_climatico.txt"},
            {"title": "El Renacimiento Fue", "author": "Fundación Kinal", "min_age": 19, "max_age": 98,
             "content_filename": "el_renacimient_fue.txt"}, # Se asume 'el_renacimiento.txt' se refiere a este
            {"title": "La Civilización Maya", "author": "Fundación Kinal", "min_age": 12, "max_age": 85,
             "content_filename": "la_civilizacion_maya.txt"},
            {"title": "La Lengua Española", "author": "Fundación Kinal", "min_age": 10, "max_age": 70,
             "content_filename": "la_lengua_espaniola.txt"},
            {"title": "La Revolución Industrial", "author": "Fundación Kinal", "min_age": 13, "max_age": 90,
             "content_filename": "la_revolucion_industrial.txt"},
            {"title": "La Revolución Francesa", "author": "Fundación Kinal", "min_age": 18, "max_age": 70,
             "content_filename": "la_revolucion_francesa.txt"},
            {"title": "Machu Picchu", "author": "Fundación Kinal", "min_age": 13, "max_age": 95,
             "content_filename": "machu_picchu.txt"},
            {"title": "Nelson Mandela", "author": "Fundación Kinal", "min_age": 18, "max_age": 95,
             "content_filename": "nelson_mandela.txt"},

            # --- Nuevos libros agregados ---
            {"title": "El Ciervo y el Manantial", "author": "Fábula Clásica", "min_age": 7, "max_age": 10,
             "content_filename": "el_ciervo_y_el_manantial.txt"},
            {"title": "La Leyenda del Maíz", "author": "Leyenda Maya", "min_age": 8, "max_age": 12,
             "content_filename": "la_leyenda_del_maiz.txt"},
            {"title": "El Hombre, el Niño y el Burro", "author": "Fábula Clásica", "min_age": 7, "max_age": 10,
             "content_filename": "el_hombre_el_ninio_y_el_burro.txt"},
            {"title": "La Llorona", "author": "Leyenda Popular", "min_age": 10, "max_age": 14,
             "content_filename": "la_llorona.txt"},
            {"title": "El Joven Rico", "author": "Relato Bíblico", "min_age": 12, "max_age": 99,
             "content_filename": "el_joven_rico.txt"},
            {"title": "La Mujer Adúltera", "author": "Relato Bíblico", "min_age": 16, "max_age": 99,
             "content_filename": "la_mujer_adultera.txt"},
            {"title": "El León y el Ratón", "author": "Fábula de Esopo", "min_age": 6, "max_age": 9,
             "content_filename": "el_leon_y_el_raton.txt"},
            {"title": "La Cruz como Camino", "author": "Fundación Kinal", "min_age": 16, "max_age": 99,
             "content_filename": "la_cruz_como_camino.txt"},
            {"title": "Pedro y el Lobo", "author": "Sergei Prokofiev", "min_age": 6, "max_age": 9,
             "content_filename": "pedro_y_el_lobo.txt"},
            {"title": "El Buen Samaritano", "author": "Relato Bíblico", "min_age": 10, "max_age": 99,
             "content_filename": "el_buen_samaritano.txt"},
            {"title": "El Pan Compartido", "author": "Fábula Clásica", "min_age": 7, "max_age": 10,
             "content_filename": "el_pan_compartido.txt"},
            {"title": "La Cultura Japonesa", "author": "Fundación Kinal", "min_age": 14, "max_age": 99,
             "content_filename": "la_cultura_japonesa.txt"},
            {"title": "El Cadejo", "author": "Leyenda Guatemalteca", "min_age": 12, "max_age": 99,
             "content_filename": "el_cadejo.txt"},
            {"title": "El Traje Nuevo del Emperador", "author": "Hans Christian Andersen", "min_age": 7, "max_age": 11,
             "content_filename": "el_traje_nuevo_del_emperador.txt"},
            {"title": "La Gallina de los Huevos de Oro", "author": "Fábula de Esopo", "min_age": 6, "max_age": 9,
             "content_filename": "la_gallina_de_los_huevos_de_oro.txt"},
            {"title": "La Zorra y las Uvas", "author": "Fábula de Esopo", "min_age": 7, "max_age": 10,
             "content_filename": "la_zorra_y_las_uvas.txt"},
        ]

        conn = self._get_connection()
        cursor = conn.cursor()

        for book_data in books_to_insert:
            # content_path_relative es la ruta tal como la quieres almacenar en la BD.
            # Esta ruta DEBE coincidir con cómo se estructuran los archivos de libros DENTRO del paquete.
            # Según tu .spec, los copias a 'src/books_content/'.
            content_path_relative = os.path.join("src", "books_content", book_data["content_filename"])

            cursor.execute("SELECT id FROM books WHERE content_path = ?", (content_path_relative,))
            existing_book = cursor.fetchone()

            if not existing_book:
                word_count = self._get_word_count_from_file(
                    book_data["content_filename"])  # Pasamos solo el nombre del archivo
                cursor.execute(
                    """INSERT INTO books (title, author, min_age, max_age, content_path, word_count)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (book_data["title"], book_data["author"], book_data["min_age"],
                     book_data["max_age"], content_path_relative, word_count)  # Guarda la ruta relativa
                )
                print(f"Libro '{book_data['title']}' insertado.")
            else:
                print(f"Libro '{book_data['title']}' ya existe.")
        conn.commit()
        conn.close()

    def _get_word_count_from_file(self, filename):
        # BOOKS_DIRECTORY ya es la ruta ABSOLUTA correcta definida en config.py
        full_file_path = os.path.join(BOOKS_DIRECTORY, filename)

        if not os.path.exists(full_file_path):
            print(f"Advertencia: Archivo de contenido no encontrado para conteo de palabras: {full_file_path}")
            return 0  # Si el archivo no existe, el conteo de palabras es 0
        try:
            with open(full_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return len(content.split())
        except Exception as e:
            print(f"Error al leer el archivo para conteo de palabras {full_file_path}: {e}")
            return 0

    def add_user(self, age):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (age) VALUES (?)", (age,))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id

    def get_recommended_books(self, age):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, title, author, min_age, max_age, content_path, word_count
               FROM books
               WHERE ? BETWEEN min_age AND max_age
               ORDER BY title""",
            (age,)
        )
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books

    def get_book_info(self, book_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, title, author, min_age, max_age, content_path, word_count
               FROM books WHERE id = ?""",
            (book_id,)
        )
        book_info = cursor.fetchone()
        conn.close()
        return dict(book_info) if book_info else None

    def start_reading_session(self, user_id, book_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO reading_sessions (user_id, book_id, start_time)
               VALUES (?, ?, datetime('now'))""",
            (user_id, book_id)
        )
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"Sesión de lectura iniciada. ID: {session_id}")
        return session_id

    def finish_reading_session(self, session_id, duration_seconds, wpm, age_appropriateness_score, performance_rating,
                               quiz_score=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE reading_sessions SET
                end_time = datetime('now'),
                duration_seconds = ?,
                wpm = ?,
                age_appropriateness_score = ?,
                performance_rating = ?,
                quiz_score = ?
            WHERE id = ?""",
            (duration_seconds, wpm, age_appropriateness_score, performance_rating, quiz_score, session_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def get_user_reading_stats(self, user_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT
                rs.start_time,
                rs.duration_seconds,
                rs.wpm,
                rs.performance_rating,
                rs.quiz_score,
                b.title AS book_title,
                b.author AS book_author
            FROM reading_sessions rs
            JOIN books b ON rs.book_id = b.id
            WHERE rs.user_id = ?
            ORDER BY rs.start_time DESC""",
            (user_id,)
        )
        stats = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return stats
