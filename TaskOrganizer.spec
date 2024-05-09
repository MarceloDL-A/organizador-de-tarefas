# TaskOrganizer.spec

# -*- mode: python -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_submodules

# Coleta todos os submódulos
models_submodules = collect_submodules('models')
ui_submodules = collect_submodules('ui')
utils_submodules = collect_submodules('utils')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('models/*.py', 'models'),
        ('ui/*.py', 'ui'),
        ('utils/*.py', 'utils'),
        ('tasks.json', '.'),
        ('task_history.txt', '.'),
    ],
    hiddenimports=[
        'ttkthemes',
        'mistletoe',
        *models_submodules,
        *ui_submodules,
        *utils_submodules
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TaskOrganizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TaskOrganizer'
)
