import os
import sys
import PyInstaller.__main__

def build():
    APP_NAME = "Soft_BG_Remover_v2.0"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Separador de caminho (; para Windows, : para Unix)
    sep = ';' if os.name == 'nt' else ':'

    # Arquivos e pastas para incluir
    # (arquivo_origem, pasta_destino_no_exe)
    includes = [
        ('config.json', '.'),
        ('ui', 'ui'),
        ('utils', 'utils'),
        ('app_icon.ico', '.'),
        ('softsafe_favicon.ico', '.'),
    ]
    
    # Incluir modelo IA se existir (recomendado para modo offline)
    if os.path.exists(os.path.join(base_dir, 'u2net.onnx')):
        includes.append(('u2net.onnx', '.'))
    else:
        print("⚠️  Aviso: u2net.onnx não encontrado. O executável tentará baixá-lo na primeira execução.")

    # Montar argumentos --add-data
    add_data = []
    for src, dst in includes:
        if os.path.exists(os.path.join(base_dir, src)):
            add_data.append(f'--add-data={src}{sep}{dst}')

    # Verificar se existe imagem de splash
    splash_args = []
    if os.path.exists(os.path.join(base_dir, 'splash.png')):
        splash_args.append('--splash=splash.png')
        print("💧 Splash screen encontrada: splash.png")

    args = [
        'launcher.py',  # Alterado de app.py para launcher.py
        f'--name={APP_NAME}',
        '--noconfirm',
        '--windowed',
        '--clean',
        '--icon=app_icon.ico',
        # Coletar dependências complexas automaticamente
        '--collect-all=customtkinter',
        '--collect-all=rembg',
        '--onefile', # Cria um único arquivo .exe
    ] + add_data + splash_args

    print(f"🔨 Iniciando compilação do {APP_NAME}...")
    PyInstaller.__main__.run(args)
    print(f"\n✅ Sucesso! Executável criado em: dist/{APP_NAME}.exe")

if __name__ == "__main__":
    build()