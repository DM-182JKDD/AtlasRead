# AtlasRead.spec

# -*- mode: python ; coding: utf-8 -*-

import sys
import os
import customtkinter # PyInstaller necesita que este módulo sea accesible para encontrar su ruta

# --- NUEVO: Obtener la ruta de la instalación de customtkinter ---
# Esto es para asegurar que PyInstaller incluya todos los assets de customtkinter.
try:
    customtkinter_path = os.path.dirname(customtkinter.__file__)
except ImportError:
    print("Error: customtkinter no se encontró. Asegúrate de que tu entorno virtual esté activado y customtkinter instalado.")
    sys.exit(1)
# --- FIN NUEVO ---


a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('atlasread.db', '.'),
        ('src/books_content', 'src/books_content'),
        ('src/quizzes', 'src/quizzes'),
        (customtkinter_path, 'customtkinter'),
    ],
    hiddenimports=['Pillow', 'tkinter', 'customtkinter', 'PIL._tkinter_finder'], # <--- ¡CAMBIO AQUÍ!
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AtlasRead',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AtlasRead',
)