# src/logic.py

import os
import json
from src.config import WPM_EXPECTED, BOOKS_DIRECTORY, QUIZZES_DIRECTORY


class AppLogic:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_recommended_books(self, age):
        return self.db_manager.get_recommended_books(age)

    def read_book_content(self, relative_path_from_project_root):
        # relative_path_from_project_root es la ruta almacenada en la DB (ej. "src/books_content/patito_feo.txt")
        # BOOKS_DIRECTORY ya es la ruta ABSOLUTA base para tus libros.
        # Entonces, solo necesitas obtener el nombre del archivo y unirlo a BOOKS_DIRECTORY.
        filename = os.path.basename(relative_path_from_project_root)
        full_path = os.path.join(BOOKS_DIRECTORY, filename)

        if not os.path.exists(full_path):
            print(f"Error: El archivo de contenido no fue encontrado en: {full_path}")
            return "Contenido del libro no disponible."
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error al leer el archivo {full_path}: {e}")
            return "Error al cargar el contenido del libro."

    def load_quiz_for_book(self, book_id):
        """Carga el cuestionario para un libro dado su ID."""
        book_info = self.db_manager.get_book_info(book_id)
        if not book_info:
            return None

        content_filename = os.path.basename(book_info['content_path'])  # Obtener solo el nombre del archivo del libro
        quiz_filename = os.path.splitext(content_filename)[0] + ".json"  # Construir el nombre del archivo del quiz

        # QUIZZES_DIRECTORY ya es la ruta ABSOLUTA base para tus quizzes
        full_quiz_path = os.path.join(QUIZZES_DIRECTORY, quiz_filename)

        if not os.path.exists(full_quiz_path):
            print(f"No se encontró cuestionario para {book_info['title']} en {full_quiz_path}")
            return None
        try:
            with open(full_quiz_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON del quiz {full_quiz_path}: {e}")
            return None
        except Exception as e:
            print(f"Error al cargar el quiz {full_quiz_path}: {e}")
            return None

    def calculate_reading_stats(self, user_age, book_word_count, duration_seconds):
        if duration_seconds == 0:
            actual_wpm = 0
        else:
            actual_wpm = (book_word_count / duration_seconds) * 60

        expected_wpm_range = WPM_EXPECTED.get(user_age)
        if not expected_wpm_range:
            expected_wpm_range = WPM_EXPECTED.get('default')

        min_wpm, max_wpm = expected_wpm_range

        if actual_wpm >= min_wpm and actual_wpm <= max_wpm:
            age_appropriateness_score = 100.0
            performance_rating = "Normal"
        elif actual_wpm < min_wpm:
            age_appropriateness_score = max(0, (actual_wpm / min_wpm) * 100)
            performance_rating = "Necesita mejorar (Lento)"
        else:  # actual_wpm > max_wpm
            if actual_wpm > max_wpm * 1.2:
                age_appropriateness_score = 100.0 - ((actual_wpm - max_wpm) / max_wpm) * 20
                performance_rating = "Rápido"
            else:
                age_appropriateness_score = 100.0
                performance_rating = "Rápido"
        return actual_wpm, age_appropriateness_score, performance_rating

    def evaluate_quiz(self, quiz_data, user_answers):
        correct_count = 0
        total_questions = len(quiz_data['questions'])

        for q in quiz_data['questions']:
            question_id = str(q['id'])
            correct_answer_id = str(q['correct_answer'])

            if question_id in user_answers:
                if str(user_answers[question_id]) == correct_answer_id:
                    correct_count += 1
        return correct_count, total_questions