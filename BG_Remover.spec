# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# --- COLETA AUTOMÁTICA DE DEPENDÊNCIAS COMPLEXAS ---
datas = []
binaries = []
hiddenimports = []

# 1. Coleta tudo do CustomTkinter (temas, configurações)
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# 2. Coleta tudo do TkinterDnD2 (binários de drag & drop)
tmp_ret = collect_all('tkinterdnd2')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# 3. Adiciona seus arquivos manuais (Modelo IA, Config, Ícones)
# Formato: ('arquivo_origem', 'pasta_destino_no_exe')
datas += [
    ('u2net.onnx', '.'),
    ('config.json', '.'),
    ('app_icon.ico', '.'),
    ('softsafe_favicon.ico', '.'),
]

# --- ANÁLISE DO PROJETO ---
a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --- CRIAÇÃO DO EXECUTÁVEL ---
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Soft BG Remover',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # <--- False para não abrir aquela tela preta de terminal
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
)

# --- MONTAGEM DA PASTA FINAL ---
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Soft BGRemover',
    icon='app_icon.ico',
)