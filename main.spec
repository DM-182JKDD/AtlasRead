# -*- mode: python ; coding: utf-8 -*-
import glob

# Archivos .txt en src/books_content
txt_files = glob.glob('src/books_content/*.txt')
# Archivos .json en src/quizzes
json_files = glob.glob('src/quizzes/*.json')

datas = [(f, 'src/books_content') for f in txt_files] + [(f, 'src/quizzes') for f in json_files]

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    console=False,
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
