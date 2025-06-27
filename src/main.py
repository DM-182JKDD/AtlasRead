# src/main.py

from src.gui import AtlasReadApp
from src.database import DatabaseManager
from src.logic import AppLogic
import os

if __name__ == "__main__":
    # Inicializar el manejador de la base de datos
    db_manager = DatabaseManager()

    # Inicializar la lógica de la aplicación
    app_logic = AppLogic(db_manager)

    # Crear y ejecutar la aplicación GUI
    app = AtlasReadApp(db_manager, app_logic)
    app.mainloop()

