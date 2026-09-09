# PyInstaller configuration for Boxing Film Generator
# This packages the application as a standalone Windows executable

# Install PyInstaller first:
# pip install pyinstaller

# Then run this command:
# pyinstaller boxing_film_generator.spec

# The executable will be in: dist/BoxingFilmGenerator/BoxingFilmGenerator.exe

# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[str(Path.cwd())],
    binaries=[],
    datas=[
        ('src/prompts', 'src/prompts'),
        ('config', 'config'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'openai',
        'pydantic',
        'pydantic_settings',
        'aiohttp',
        'click',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BoxingFilmGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
