@echo off
echo ============================================
echo Eliminando carpetas antiguas de compilacion...
echo ============================================
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q __pycache__

echo ============================================
echo Eliminando entorno virtual antiguo...
echo ============================================
rmdir /s /q .venv

echo ============================================
echo Creando nuevo entorno virtual...
echo ============================================
python -m venv .venv

echo ============================================
echo Activando entorno virtual...
echo ============================================
call .\.venv\Scripts\activate

echo ============================================
echo Instalando dependencias...
echo ============================================
pip install --upgrade pip
pip install -r requirements.txt

echo ============================================
echo Compilando con PyInstaller y main.spec...
echo ============================================
pyinstaller --clean main.spec

echo ============================================
echo TODO LISTO! Ejecutable generado en dist\main
echo ============================================

pause
