import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from src.logic import AppLogic
from src.database import DatabaseManager
from src.config import APP_NAME
import datetime
import os
import sys


class AtlasReadApp(ctk.CTk):
    def __init__(self, db_manager, app_logic):
        super().__init__()
        self.db_manager = db_manager
        self.app_logic = app_logic

        self.user_id = None
        self.user_age = None
        self.current_reading_session_id = None
        self.current_book = None
        self.reading_start_time = None
        self.current_quiz_data = None
        self.user_quiz_answers = {}
        self._temp_stats = {}  # Para guardar stats temporales antes del quiz

        # --- Configuración Global de CustomTkinter ---
        ctk.set_appearance_mode("Light")  # Modo claro para la base (esencial para la nueva paleta)
        ctk.set_default_color_theme("blue")  # El tema por defecto, aunque lo sobrescribimos

        # --- Definición de Colores de la Paleta (Educativo Moderno y Cálido) ---
        self.COLOR_BACKGROUND_MAIN = "#F8F9FA"  # Un blanco casi puro, muy suave
        self.COLOR_TEXT_PRIMARY = "#343A40"  # Gris oscuro casi negro
        self.COLOR_TEXT_SECONDARY = "#6C757D"  # Gris medio
        self.COLOR_ACCENT_PRIMARY = "#4CAF50"  # Verde vibrante (antes era el principal, ahora lo reservamos)
        self.COLOR_ACCENT_SECONDARY = "#2196F3"  # Azul amigable (ahora será el color principal de los botones)

        # Colores específicos para elementos interactivos y bordes
        self.COLOR_BUTTON_NORMAL = "#E9ECEF"  # Gris muy claro para el fondo de los botones (similar al fondo alternativo)
        self.COLOR_BUTTON_HOVER = "#DEE2E6"  # Un gris ligeramente más oscuro para el hover
        self.COLOR_BUTTON_TEXT = "#343A40"  # Negro para el texto de los botones
        self.COLOR_BORDER = "#DEE2E6"  # Gris muy claro y sutil para los bordes

        # Colores para estados (rendimiento, quiz, mensajes)
        self.COLOR_PERFORMANCE_EXCELLENT = "#4CAF50"  # Verde para excelente
        self.COLOR_PERFORMANCE_GOOD = "#8BC34A"  # Verde lima suave para bueno
        self.COLOR_PERFORMANCE_OK = "#FFC107"  # Amarillo ámbar para aceptable/regular
        self.COLOR_PERFORMANCE_BAD = "#EF5350"  # Rojo suave para necesita mejorar

        self.COLOR_QUIZ_PASS = "#4CAF50"  # Verde para quiz aprobado
        self.COLOR_QUIZ_FAIL = "#EF5350"  # Rojo para quiz reprobado

        # --- Definición de Fuentes (usando tuplas directamente) ---
        self.FONT_TITLE = ("Segoe UI", 30, "bold")
        self.FONT_SUBTITLE = ("Segoe UI", 20, "bold")  # Renombrado de FONT_HEADING
        self.FONT_BODY = ("Segoe UI", 16)
        self.FONT_BUTTON = ("Segoe UI", 16, "bold")
        self.FONT_SMALL = ("Segoe UI", 12)
        self.FONT_MONOSPACE = ("Courier New", 14)  # Para texto de libro si se desea un estilo más fijo
        self.FONT_ERROR = ("Segoe UI", 12, "bold")  # Fuente específica para mensajes de error

        # --- Configuración de la Ventana Principal ---
        self.title(APP_NAME)
        self.geometry("900x700")
        self.minsize(700, 550)
        self.configure(fg_color=self.COLOR_BACKGROUND_MAIN)  # Usar el color principal para la ventana

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Inicialización de todos los marcos una sola vez ---
        self.frames = {}
        # Los frames se inicializan con sus propios colores de fondo
        self._create_start_frame()  # Nuevo: Frame de inicio
        self._create_age_input_frame()
        self._create_book_selection_frame()
        self._create_reading_frame()
        self._create_quiz_frame()
        self._create_statistics_frame()

        # Mostrar el frame inicial al principio
        self.show_frame("start")  # Cambiado para iniciar en el frame de bienvenida

    def show_frame(self, name):
        """Oculta todos los marcos y muestra solo el especificado."""
        for frame_name, frame_widget in self.frames.items():
            frame_widget.grid_forget()  # Oculta el marco

        if name in self.frames:
            # Padding general alrededor de los frames dentro de la ventana principal
            self.frames[name].grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

            # Configurar columna y fila 0 en el marco para que se expandan
            self.frames[name].grid_columnconfigure(0, weight=1)
            # Cada frame configura sus propias filas, pero nos aseguramos que haya al menos una para el contenido principal
            self.frames[name].grid_rowconfigure(0, weight=1)

            # Ajustes específicos para ciertos marcos que necesitan más filas configurables
            if name == "start":
                # Configurar para centrar contenido en el frame de inicio
                self.frames[name].grid_rowconfigure((0, 4), weight=1)  # Espacio arriba y abajo
                self.frames[name].grid_columnconfigure(0, weight=1)
            elif name == "age_input":
                self.frames[name].grid_rowconfigure((0, 6), weight=1)  # Más espacio arriba y abajo para centrar
                self.frames[name].grid_rowconfigure((1, 2, 3, 4, 5), weight=0)  # Contenido fijo
                self.frames[name].grid_columnconfigure(0, weight=1)
            elif name == "book_selection":
                self.frames[name].grid_rowconfigure(0, weight=0)  # Título
                self.frames[name].grid_rowconfigure(1, weight=1)  # Contenedor de libros (scrollable)
                self.frames[name].grid_rowconfigure(2, weight=0)  # Botones de navegación
                self.frames[name].grid_columnconfigure(0, weight=1)
            elif name == "reading":
                self.frames[name].grid_rowconfigure(0, weight=0)  # Título
                self.frames[name].grid_rowconfigure(1, weight=1)  # Textbox del libro
                self.frames[name].grid_rowconfigure(2, weight=0)  # Botón "terminar lectura"
                self.frames[name].grid_columnconfigure(0, weight=1)
            elif name == "quiz":
                self.frames[name].grid_rowconfigure(0, weight=0)  # Título
                self.frames[name].grid_rowconfigure(1, weight=1)  # Preguntas del quiz (scrollable)
                self.frames[name].grid_rowconfigure(2, weight=0)  # Botón "enviar"
                self.frames[name].grid_columnconfigure(0, weight=1)
            elif name == "statistics":
                self.frames[name].grid_rowconfigure(0, weight=0)  # Title
                self.frames[name].grid_rowconfigure(1, weight=0)  # Explanation frame
                self.frames[name].grid_rowconfigure(2, weight=1)  # Scrollable frame (table)
                self.frames[name].grid_rowconfigure(3, weight=0)  # Buttons

    # --- Nuevo método de creación de marco de inicio ---
    def _create_start_frame(self):
        frame = ctk.CTkFrame(self, fg_color=self.COLOR_BACKGROUND_MAIN)
        self.frames["start"] = frame

        # Widgets para el frame de inicio
        app_name_label = ctk.CTkLabel(frame, text=APP_NAME, font=self.FONT_TITLE, text_color=self.COLOR_TEXT_PRIMARY)
        app_name_label.grid(row=1, column=0, pady=(50, 20))  # Ajustar padding

        start_button = ctk.CTkButton(
            frame, text="Empezar", command=self.show_age_input_frame,  # Cambiado a show_age_input_frame
            font=self.FONT_BUTTON,
            fg_color=self.COLOR_ACCENT_SECONDARY,  # Botón azul principal
            text_color="white",  # Texto blanco para botones azules
            hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10),  # Oscurecer al pasar el mouse
            corner_radius=8, border_width=1, border_color=self.COLOR_ACCENT_SECONDARY
            # Borde del mismo color para realzar
        )
        start_button.grid(row=2, column=0, pady=10)

        quit_button = ctk.CTkButton(
            frame, text="Salir", command=self.quit_application,
            font=self.FONT_BUTTON,
            fg_color=self.COLOR_BUTTON_NORMAL,  # Color neutro para salir
            text_color=self.COLOR_TEXT_PRIMARY,  # Texto oscuro para botones neutros
            hover_color=self.COLOR_BUTTON_HOVER,
            corner_radius=8, border_width=1, border_color=self.COLOR_BORDER
        )
        quit_button.grid(row=3, column=0, pady=10)

    # --- Métodos de creación de marcos (llamados solo una vez en __init__) ---
    def _create_age_input_frame(self):
        frame = ctk.CTkFrame(self, fg_color=self.COLOR_BACKGROUND_MAIN)
        self.frames["age_input"] = frame

        # Widgets para el frame de entrada de edad
        welcome_title_label = ctk.CTkLabel(
            frame, text=f"Bienvenido a {APP_NAME}", font=self.FONT_TITLE,
            text_color=self.COLOR_TEXT_PRIMARY
        )
        welcome_title_label.grid(row=1, column=0, pady=(10, 20))

        age_input_label = ctk.CTkLabel(
            frame, text="Por favor, ingresa tu edad:", font=self.FONT_SUBTITLE,
            text_color=self.COLOR_TEXT_PRIMARY
        )
        age_input_label.grid(row=2, column=0, pady=(0, 20))

        self.age_entry = ctk.CTkEntry(
            frame, width=200, placeholder_text="Edad", font=self.FONT_BODY,
            text_color=self.COLOR_TEXT_PRIMARY,  # Texto primario para la entrada
            fg_color=self.COLOR_BUTTON_NORMAL,  # Fondo claro para el entry (como un campo de texto)
            border_color=self.COLOR_ACCENT_SECONDARY,  # Borde con color de acento secundario
            corner_radius=8, border_width=1, justify="center"
        )
        self.age_entry.grid(row=3, column=0, pady=(0, 5))

        self.age_error_label = ctk.CTkLabel(
            frame, text="", font=self.FONT_ERROR, text_color=self.COLOR_PERFORMANCE_BAD  # Usar color de error
        )
        self.age_error_label.grid(row=4, column=0, pady=(0, 10))

        submit_button = ctk.CTkButton(
            frame, text="Continuar", command=self.process_age_input, font=self.FONT_BUTTON,
            fg_color=self.COLOR_ACCENT_SECONDARY,  # Botón azul principal
            text_color="white",
            hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10),
            corner_radius=8, border_width=1, border_color=self.COLOR_ACCENT_SECONDARY
        )
        submit_button.grid(row=5, column=0, pady=(0, 40))

    def _create_book_selection_frame(self):
        frame = ctk.CTkFrame(self, fg_color=self.COLOR_BACKGROUND_MAIN)
        self.frames["book_selection"] = frame

        # Título
        self.book_selection_title_label = ctk.CTkLabel(  # Etiqueta para actualizar dinámicamente
            frame, text="", font=self.FONT_SUBTITLE, text_color=self.COLOR_TEXT_PRIMARY
        )
        self.book_selection_title_label.grid(row=0, column=0, pady=(10, 15))

        # Contenedor para los libros (scrollable)
        self.book_cards_container = ctk.CTkScrollableFrame(
            frame, fg_color=self.COLOR_BACKGROUND_MAIN, corner_radius=8, border_width=0,  # Sin borde principal
            scrollbar_button_color=self.COLOR_ACCENT_SECONDARY,
            scrollbar_button_hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10)
        )
        self.book_cards_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)  # Mayor padx/pady aquí
        self.book_cards_container.grid_columnconfigure(0, weight=1)

        # Botones de navegación
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")  # Fondo transparente para agrupar botones
        button_frame.grid(row=2, column=0, pady=(10, 20))
        button_frame.grid_columnconfigure((0, 1), weight=1)  # Para distribuir los botones

        ctk.CTkButton(
            button_frame, text="Cambiar Edad", command=self.show_age_input_frame,
            font=self.FONT_BUTTON,
            fg_color=self.COLOR_BUTTON_NORMAL,
            text_color=self.COLOR_TEXT_PRIMARY,
            hover_color=self.COLOR_BUTTON_HOVER,
            corner_radius=8, border_width=1, border_color=self.COLOR_BORDER
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            button_frame, text="Ver Estadísticas", command=self.show_statistics_frame,
            font=self.FONT_BUTTON,
            fg_color=self.COLOR_BUTTON_NORMAL,
            text_color=self.COLOR_TEXT_PRIMARY,
            hover_color=self.COLOR_BUTTON_HOVER,
            corner_radius=8, border_width=1, border_color=self.COLOR_BORDER
        ).grid(row=0, column=1, padx=10)

    def _create_reading_frame(self):
        frame = ctk.CTkFrame(self, fg_color=self.COLOR_BACKGROUND_MAIN)
        self.frames["reading"] = frame

        # Título del libro
        self.reading_title_label = ctk.CTkLabel(  # Etiqueta para actualizar dinámicamente
            frame, text="", font=self.FONT_SUBTITLE, text_color=self.COLOR_TEXT_PRIMARY
        )
        self.reading_title_label.grid(row=0, column=0, pady=(10, 10))

        self.book_text_widget = ctk.CTkTextbox(  # Contenido del libro
            frame, wrap="word", font=self.FONT_BODY,
            text_color=self.COLOR_TEXT_PRIMARY,  # Texto principal
            fg_color=self.COLOR_BUTTON_NORMAL,  # Fondo claro para el texto (simula papel)
            corner_radius=8, border_width=1,
            border_color=self.COLOR_BORDER,  # Borde sutil
            scrollbar_button_color=self.COLOR_ACCENT_SECONDARY,
            scrollbar_button_hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10)
        )
        self.book_text_widget.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)  # Mayor padx
        self.book_text_widget.configure(state="disabled")  # No editable por el usuario

        ctk.CTkButton(
            frame, text="He Terminado de Leer", command=self.finish_reading, font=self.FONT_BUTTON,
            fg_color=self.COLOR_ACCENT_SECONDARY,  # Botón azul principal
            text_color="white",
            hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10),
            corner_radius=8, border_width=1, border_color=self.COLOR_ACCENT_SECONDARY
        ).grid(row=2, column=0, pady=(10, 20))

    def _create_quiz_frame(self):
        frame = ctk.CTkFrame(self, fg_color=self.COLOR_BACKGROUND_MAIN)
        self.frames["quiz"] = frame

        # Título del cuestionario
        self.quiz_title_label = ctk.CTkLabel(  # Etiqueta para actualizar dinámicamente
            frame, text="", font=self.FONT_SUBTITLE, text_color=self.COLOR_TEXT_PRIMARY
        )
        self.quiz_title_label.grid(row=0, column=0, pady=(10, 15))

        self.scrollable_questions_frame = ctk.CTkScrollableFrame(  # Contenedor para preguntas del quiz
            frame, fg_color=self.COLOR_BACKGROUND_MAIN, corner_radius=8, border_width=0,
            scrollbar_button_color=self.COLOR_ACCENT_SECONDARY,
            scrollbar_button_hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10)
        )
        self.scrollable_questions_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)  # Mayor padx
        self.scrollable_questions_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            frame, text="Enviar Respuestas", command=self.process_quiz_answers, font=self.FONT_BUTTON,
            fg_color=self.COLOR_ACCENT_SECONDARY,  # Botón azul principal
            text_color="white",
            hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10),
            corner_radius=8, border_width=1, border_color=self.COLOR_ACCENT_SECONDARY
        ).grid(row=2, column=0, pady=(10, 20))

    def _create_statistics_frame(self):
        frame = ctk.CTkFrame(self, fg_color=self.COLOR_BACKGROUND_MAIN)
        self.frames["statistics"] = frame

        # Título de estadísticas
        ctk.CTkLabel(
            frame, text="Tus Estadísticas de Lectura", font=self.FONT_SUBTITLE, text_color=self.COLOR_TEXT_PRIMARY
        ).grid(row=0, column=0, pady=(10, 15))

        # --- Explicación de Métricas ---
        explanation_frame = ctk.CTkFrame(
            frame, fg_color=self.COLOR_BUTTON_NORMAL,  # Fondo claro para el panel de explicación
            corner_radius=8, border_width=1,
            border_color=self.COLOR_BORDER
        )
        explanation_frame.grid(row=1, column=0, pady=(0, 15), padx=50, sticky="ew")
        explanation_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            explanation_frame, text="Explicación de Métricas:", font=self.FONT_BUTTON,  # Fuente de botón para subtítulo
            text_color=self.COLOR_TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))
        ctk.CTkLabel(
            explanation_frame, text="• WPM: Palabras por minuto. Indica tu velocidad de lectura.",
            font=self.FONT_SMALL, text_color=self.COLOR_TEXT_SECONDARY, wraplength=700, justify="left"
        ).grid(row=1, column=0, sticky="w", padx=25, pady=2)
        ctk.CTkLabel(
            explanation_frame,
            text="• Rendimiento: Evalúa si tu velocidad de lectura es apropiada para tu edad (Verde: Normal/Rápido, Rojo: Lento).",
            font=self.FONT_SMALL, text_color=self.COLOR_TEXT_SECONDARY, wraplength=700, justify="left"
        ).grid(row=2, column=0, sticky="w", padx=25, pady=2)
        ctk.CTkLabel(
            explanation_frame, text="• Quiz: Puntuación en el cuestionario de comprensión (Verde: ≥70%, Rojo: <70%).",
            font=self.FONT_SMALL, text_color=self.COLOR_TEXT_SECONDARY, wraplength=700, justify="left"
        ).grid(row=3, column=0, sticky="w", padx=25, pady=(2, 10))

        # Contenedor para las estadísticas (actualizado dinámicamente)
        self.stats_scrollable_frame = ctk.CTkScrollableFrame(
            frame, fg_color=self.COLOR_BACKGROUND_MAIN, corner_radius=8, border_width=0,
            scrollbar_button_color=self.COLOR_ACCENT_SECONDARY,
            scrollbar_button_hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10)
        )
        self.stats_scrollable_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)  # Mayor padx
        self.stats_scrollable_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # Botones de navegación (estáticos)
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, pady=(10, 20))
        button_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            button_frame, text="Leer Otro Libro", command=self.show_book_selection_frame, font=self.FONT_BUTTON,
            fg_color=self.COLOR_ACCENT_SECONDARY,  # Botón azul principal
            text_color="white",
            hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10),
            corner_radius=8, border_width=1, border_color=self.COLOR_ACCENT_SECONDARY
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            button_frame, text="Salir", command=self.quit_application, font=self.FONT_BUTTON,
            fg_color=self.COLOR_BUTTON_NORMAL,  # Botón neutro
            text_color=self.COLOR_TEXT_PRIMARY,
            hover_color=self.COLOR_BUTTON_HOVER,
            corner_radius=8, border_width=1, border_color=self.COLOR_BORDER
        ).grid(row=0, column=1, padx=10)

    # --- Métodos que gestionan el flujo de la aplicación (ahora usan show_frame y actualizan contenido) ---
    def process_age_input(self):
        self.age_error_label.configure(text="")
        try:
            age = int(self.age_entry.get())
            if 6 <= age <= 99:
                self.user_age = age
                self.user_id = self.db_manager.add_user(self.user_age)
                if self.user_id:
                    self.show_book_selection_frame()
                else:
                    CTkMessagebox(
                        title="Error de DB", message="No se pudo registrar el usuario en la base de datos.",
                        icon="cancel", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
                    )
            else:
                self.age_error_label.configure(text="Edad inválida: Ingresa una edad entre 6 y 99 años.")
                CTkMessagebox(
                    title="Edad Inválida", message="Por favor, ingresa una edad entre 6 y 99 años.",
                    icon="warning", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
                )
        except ValueError:
            self.age_error_label.configure(text="Entrada inválida: Por favor, ingresa un número.")
            CTkMessagebox(
                title="Entrada Inválida", message="Por favor, ingresa un número válido para la edad.",
                icon="warning", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
            )

    def show_age_input_frame(self):
        self.age_entry.delete(0, ctk.END)
        self.age_error_label.configure(text="")
        self.show_frame("age_input")

    def show_book_selection_frame(self):
        self.book_selection_title_label.configure(text=f"Libros para tu edad ({self.user_age} años)")
        self.books = self.app_logic.get_recommended_books(self.user_age)

        for widget in self.book_cards_container.winfo_children():
            widget.destroy()

        if not self.books:
            ctk.CTkLabel(self.book_cards_container, text="No hay libros disponibles para tu edad.",
                         font=self.FONT_BODY, text_color=self.COLOR_TEXT_SECONDARY).grid(row=0, column=0, pady=20)
        else:
            for i, book in enumerate(self.books):
                book_card_frame = ctk.CTkFrame(
                    self.book_cards_container, fg_color=self.COLOR_BUTTON_NORMAL,
                    # Fondo claro para las tarjetas de libro
                    corner_radius=8, border_width=1,
                    border_color=self.COLOR_BORDER
                )
                book_card_frame.grid(row=i, column=0, sticky="ew", pady=7, padx=7)
                book_card_frame.grid_columnconfigure(0, weight=1)
                book_card_frame.grid_columnconfigure(1, weight=0)

                ctk.CTkLabel(book_card_frame, text=f"{book['title']}", font=self.FONT_SUBTITLE,
                             # Subtítulo para títulos de libro
                             text_color=self.COLOR_TEXT_PRIMARY, wraplength=450, justify="left").grid(row=0, column=0,
                                                                                                      sticky="w",
                                                                                                      padx=15, pady=5)
                ctk.CTkLabel(book_card_frame, text=f"por {book['author']} | Edad: {book['min_age']}-{book['max_age']}",
                             font=self.FONT_SMALL, text_color=self.COLOR_TEXT_SECONDARY, justify="left").grid(row=1,
                                                                                                              column=0,
                                                                                                              sticky="w",
                                                                                                              padx=15,
                                                                                                              pady=2)

                select_button = ctk.CTkButton(
                    book_card_frame, text="Leer", command=lambda b=book: self.start_reading(b), font=self.FONT_BUTTON,
                    fg_color=self.COLOR_ACCENT_SECONDARY,  # Botón azul principal
                    text_color="white",
                    hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10),
                    corner_radius=8, border_width=1, border_color=self.COLOR_ACCENT_SECONDARY
                )
                select_button.grid(row=0, column=1, rowspan=2, padx=15)

        self.show_frame("book_selection")

    def start_reading(self, book):
        if self.user_id is None:
            CTkMessagebox(
                title="Error de Usuario",
                message="No se ha registrado un usuario. Por favor, reinicia la aplicación e ingresa tu edad.",
                icon="cancel", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
            )
            return

        self.current_book = book
        self.reading_start_time = datetime.datetime.now()
        self.current_reading_session_id = self.db_manager.start_reading_session(
            self.user_id, self.current_book['id']
        )
        if self.current_reading_session_id:
            self.show_reading_frame()
        else:
            CTkMessagebox(
                title="Error de Sesión",
                message="No se pudo iniciar la sesión de lectura. Por favor, inténtalo de nuevo.",
                icon="cancel", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
            )

    def show_reading_frame(self):
        self.reading_title_label.configure(text=self.current_book['title'])
        book_content = self.app_logic.read_book_content(self.current_book['content_path'])
        self.book_text_widget.configure(state="normal")
        self.book_text_widget.delete("1.0", "end")
        self.book_text_widget.insert("end", book_content)
        self.book_text_widget.configure(state="disabled")

        self.show_frame("reading")

    def finish_reading(self):
        if not self.reading_start_time or not self.current_book or not self.current_reading_session_id:
            CTkMessagebox(
                title="Error", message="No hay una sesión de lectura activa para finalizar.",
                icon="warning", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
            )
            return

        end_time = datetime.datetime.now()
        duration_seconds = int((end_time - self.reading_start_time).total_seconds())

        if duration_seconds <= 0:
            duration_seconds = 1

        book_word_count = self.current_book.get('word_count', 0)

        actual_wpm, age_appropriateness_score, performance_rating = \
            self.app_logic.calculate_reading_stats(self.user_age, book_word_count, duration_seconds)

        self._temp_stats = {
            "duration_seconds": duration_seconds,
            "wpm": actual_wpm,
            "age_appropriateness_score": age_appropriateness_score,
            "performance_rating": performance_rating
        }

        self.current_quiz_data = self.app_logic.load_quiz_for_book(self.current_book['id'])

        if self.current_quiz_data:
            self.show_quiz_frame()
        else:
            success = self.db_manager.finish_reading_session(
                self.current_reading_session_id,
                self._temp_stats["duration_seconds"],
                self._temp_stats["wpm"],
                self._temp_stats["age_appropriateness_score"],
                self._temp_stats["performance_rating"],
                None
            )
            if success:
                CTkMessagebox(
                    title="Lectura Finalizada", message="Sesión de lectura guardada con éxito (sin cuestionario).",
                    icon="info", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
                )
                self.show_statistics_frame()
            else:
                CTkMessagebox(
                    title="Error", message="No se pudo guardar la sesión de lectura.",
                    icon="cancel", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
                )

    def show_quiz_frame(self):
        if not self.current_quiz_data:
            CTkMessagebox(title="Error", message="No hay datos de cuestionario disponibles.", icon="cancel")
            self.show_statistics_frame()
            return

        self.quiz_title_label.configure(text=f"Cuestionario: {self.current_book['title']}")

        for widget in self.scrollable_questions_frame.winfo_children():
            widget.destroy()

        self.quiz_radio_vars = {}
        self.user_quiz_answers = {}

        for i, q in enumerate(self.current_quiz_data['questions']):
            question_frame = ctk.CTkFrame(
                self.scrollable_questions_frame, fg_color=self.COLOR_BUTTON_NORMAL,  # Fondo claro para cada pregunta
                corner_radius=8, border_width=1,
                border_color=self.COLOR_BORDER
            )
            question_frame.grid(row=i, column=0, sticky="ew", pady=10, padx=10)
            question_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                question_frame, text=f"P{q['id']}: {q['question']}", font=self.FONT_BUTTON,
                # Fuente de botón para la pregunta
                text_color=self.COLOR_TEXT_PRIMARY, wraplength=700, justify="left"
            ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

            self.quiz_radio_vars[str(q['id'])] = ctk.StringVar(value="")

            for j, option in enumerate(q['options']):
                rb = ctk.CTkRadioButton(
                    question_frame, text=option, variable=self.quiz_radio_vars[str(q['id'])], value=str(j + 1),
                    font=self.FONT_BODY,
                    text_color=self.COLOR_TEXT_PRIMARY,  # Texto principal para opciones
                    fg_color=self.COLOR_ACCENT_SECONDARY,  # Color del círculo del radio button
                    hover_color=self._darken_color(self.COLOR_ACCENT_SECONDARY, 10),
                    corner_radius=8  # Bordes redondeados para el radio
                )
                rb.grid(row=j + 1, column=0, sticky="w", padx=25, pady=2)

        self.show_frame("quiz")

    def process_quiz_answers(self):
        for q_id, var in self.quiz_radio_vars.items():
            self.user_quiz_answers[q_id] = var.get()

        correct_count, total_questions = self.app_logic.evaluate_quiz(
            self.current_quiz_data, self.user_quiz_answers
        )

        quiz_score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        success = self.db_manager.finish_reading_session(
            self.current_reading_session_id,
            self._temp_stats["duration_seconds"],
            self._temp_stats["wpm"],
            self._temp_stats["age_appropriateness_score"],
            self._temp_stats["performance_rating"],
            quiz_score_percentage
        )

        if success:
            CTkMessagebox(
                title="Cuestionario Finalizado",
                message=f"Has respondido correctamente {correct_count} de {total_questions} preguntas.\nTu puntuación es: {quiz_score_percentage:.2f}%",
                icon="info", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
            )
            self.show_statistics_frame()
        else:
            CTkMessagebox(
                title="Error", message="No se pudo guardar la sesión de lectura y la puntuación del cuestionario.",
                icon="cancel", fg_color=self.COLOR_BACKGROUND_MAIN, text_color=self.COLOR_TEXT_PRIMARY
            )

    def show_statistics_frame(self):
        stats = self.db_manager.get_user_reading_stats(self.user_id)

        for widget in self.stats_scrollable_frame.winfo_children():
            widget.destroy()

        if not stats:
            ctk.CTkLabel(self.stats_scrollable_frame, text="Aún no tienes sesiones de lectura registradas.",
                         font=self.FONT_BODY, text_color=self.COLOR_TEXT_SECONDARY).grid(row=0, column=0, pady=20)
        else:
            column_names = ["Libro", "Autor", "Duración", "WPM", "Rendimiento", "Quiz", "Fecha"]

            for col, name in enumerate(column_names):
                ctk.CTkLabel(self.stats_scrollable_frame, text=name, font=self.FONT_BUTTON,
                             # Fuente de botón para encabezados
                             text_color=self.COLOR_TEXT_PRIMARY, justify="center",
                             fg_color=self.COLOR_BUTTON_NORMAL,  # Fondo para los encabezados de tabla
                             corner_radius=0, padx=5, pady=5).grid(row=0, column=col, sticky="ew")

            for i, session in enumerate(stats):
                row_num = i + 1

                duration_minutes = session['duration_seconds'] // 60
                duration_seconds_remainder = session['duration_seconds'] % 60
                duration_str = f"{duration_minutes}m {duration_seconds_remainder}s"

                try:
                    start_datetime = datetime.datetime.fromisoformat(session['start_time'])
                    date_str = start_datetime.strftime("%Y-%m-%d %H:%M")
                except ValueError:
                    date_str = session['start_time']

                performance_color = self.COLOR_TEXT_PRIMARY
                if "Excelente" in session['performance_rating']:
                    performance_color = self.COLOR_PERFORMANCE_EXCELLENT
                elif "Bueno" in session['performance_rating']:
                    performance_color = self.COLOR_PERFORMANCE_GOOD
                elif "Aceptable" in session['performance_rating']:
                    performance_color = self.COLOR_PERFORMANCE_OK
                elif "Necesita mejorar" in session['performance_rating'] or "Lento" in session['performance_rating']:
                    performance_color = self.COLOR_PERFORMANCE_BAD

                quiz_score_str = f"{session['quiz_score']:.2f}%" if session['quiz_score'] is not None else "N/A"
                quiz_score_color = self.COLOR_TEXT_PRIMARY
                if session['quiz_score'] is not None:
                    if session['quiz_score'] >= 70:  # Umbral de aprobación
                        quiz_score_color = self.COLOR_QUIZ_PASS
                    else:
                        quiz_score_color = self.COLOR_QUIZ_FAIL

                row_data_values = [
                    session['book_title'],
                    session['book_author'],
                    duration_str,
                    f"{session['wpm']:.2f}",
                    session['performance_rating'],
                    quiz_score_str,
                    date_str
                ]
                row_data_colors = [
                    self.COLOR_TEXT_PRIMARY, self.COLOR_TEXT_SECONDARY, self.COLOR_TEXT_PRIMARY,
                    self.COLOR_TEXT_PRIMARY, performance_color, quiz_score_color, self.COLOR_TEXT_SECONDARY
                ]
                row_data_fonts = [self.FONT_BODY] * len(row_data_values)  # Usar fuente normal para los datos

                # Fondo de fila alternado (sutil)
                row_bg_color = self.COLOR_BACKGROUND_MAIN if i % 2 == 0 else self._darken_color(
                    self.COLOR_BACKGROUND_MAIN, 2)

                for col, data in enumerate(row_data_values):
                    ctk.CTkLabel(
                        self.stats_scrollable_frame, text=data, justify="center",
                        font=row_data_fonts[col], text_color=row_data_colors[col],
                        fg_color=row_bg_color,  # Fondo de fila
                        corner_radius=0, padx=5, pady=5
                    ).grid(row=row_num, column=col, sticky="ew")

        self.show_frame("statistics")

    def quit_application(self):
        self.destroy()

    # Métodos auxiliares para oscurecer/aclarar colores
    def _lighten_color(self, hex_color, amount):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        rgb = [min(255, int(c + (255 - c) * amount / 100)) for c in rgb]
        return "#" + "".join([f"{c:02x}" for c in rgb])

    def _darken_color(self, hex_color, amount):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        rgb = [max(0, int(c - c * amount / 100)) for c in rgb]
        return "#" + "".join([f"{c:02x}" for c in rgb])