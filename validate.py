#!/usr/bin/env python3
"""
Script de Validação - Soft BG Remover
Verifica se todas as dependências estão corretas e o programa está pronto
"""

import sys
import importlib
from pathlib import Path

def check_module(module_name, display_name=None):
    """Verifica se um módulo está instalado"""
    display_name = display_name or module_name
    try:
        mod = importlib.import_module(module_name)
        version = getattr(mod, '__version__', 'desconhecida')
        print(f"✅ {display_name}: {version}")
        return True
    except ImportError as e:
        print(f"❌ {display_name}: NÃO INSTALADO")
        print(f"   Instale com: pip install {module_name}")
        return False

def check_file(file_path, description):
    """Verifica se um arquivo existe"""
    if Path(file_path).exists():
        size = Path(file_path).stat().st_size
        size_mb = size / (1024*1024)
        print(f"✅ {description}: {size_mb:.1f}MB")
        return True
    else:
        print(f"❌ {description}: NÃO ENCONTRADO")
        return False

def main():
    print("=" * 60)
    print("🔍 VALIDAÇÃO - Soft BG Remover v2.0")
    print("=" * 60)
    
    # 1. Verificar Python
    print(f"\n📦 Python: {sys.version.split()[0]} ({'✅ OK' if sys.version_info >= (3, 10) else '❌ VERSÃO ANTIGA'})")
    
    # 2. Verificar dependências críticas
    print("\n📚 DEPENDÊNCIAS CRÍTICAS:")
    deps_ok = True
    deps_ok &= check_module('customtkinter', 'CustomTkinter')
    deps_ok &= check_module('tkinterdnd2', 'TkinterDnD2')
    deps_ok &= check_module('rembg', 'RemBG')
    deps_ok &= check_module('PIL', 'Pillow')
    deps_ok &= check_module('onnxruntime', 'ONNX Runtime')
    
    # 3. Verificar dependências opcionais
    print("\n📦 DEPENDÊNCIAS OPCIONAIS:")
    check_module('cv2', 'OpenCV')
    check_module('numpy', 'NumPy')
    check_module('scipy', 'SciPy')
    
    # 4. Verificar arquivo do modelo IA
    print("\n🤖 MODELO IA:")
    model_ok = check_file('u2net.onnx', 'Modelo U2NET (u2net.onnx)')
    
    # 5. Verificar configuração
    print("\n⚙️ CONFIGURAÇÃO:")
    config_ok = check_file('config.json', 'Arquivo de config')
    
    # 6. Verificar script principal
    print("\n📄 ARQUIVOS PRINCIPAIS:")
    app_ok = check_file('app.py', 'Aplicativo principal (app.py)')
    
    # 7. Verificar estrutura completa do projeto
    print("\n📂 ESTRUTURA DO PROJETO:")
    structure_ok = True
    project_files = [
        "config_manager.py",
        "processing.py",
        "reporting.py",
        "ui/__init__.py",
        "ui/components/__init__.py",
        "ui/components/futuristic_scrollbar.py",
        "ui/components/loading_spinner.py",
        "ui/components/tooltip.py",
        "ui/screens/__init__.py",
        "ui/screens/editor_screen.py",
        "ui/screens/home_screen.py",
        "utils/__init__.py",
        "utils/animator.py",
        "utils/colors.py",
        "utils/paths.py"
    ]
    for f in project_files:
        structure_ok &= check_file(f, f)

    # 8. Verificar assets (Ícones)
    print("\n🎨 ASSETS:")
    assets_ok = True
    assets_ok &= check_file('app_icon.ico', 'Ícone do App')
    assets_ok &= check_file('softsafe_favicon.ico', 'Favicon')

    # Resumo
    print("\n" + "=" * 60)
    if deps_ok and model_ok and app_ok and structure_ok and assets_ok:
        print("✅ TUDO OK! O programa está pronto para usar.")
        print("   Inicie com: python app.py")
        return 0
    else:
        print("⚠️  ATENÇÃO! Há problemas que precisam ser corrigidos.")
        if not deps_ok:
            print("   - Instale as dependências faltantes")
        if not model_ok:
            print("   - Baixe o modelo u2net.onnx (~175MB)")
        if not structure_ok:
            print("   - Verifique a estrutura de arquivos do projeto")
        if not assets_ok:
            print("   - Verifique se os arquivos .ico estão na pasta raiz")
        return 1

if __name__ == "__main__":
    sys.exit(main())
