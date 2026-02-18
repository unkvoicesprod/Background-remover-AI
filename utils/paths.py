import os
import sys

def resource_path(relative_path: str) -> str:
    """ Retorna o caminho absoluto para recursos, funcionando no script e no .exe """
    try:
        # O PyInstaller cria uma pasta temporária em _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

MODEL_NAME = "u2net.onnx"
MODEL_PATH = resource_path(MODEL_NAME)
ICON_PATH = resource_path("app_icon.ico")
FAVICON_PATH = resource_path("softsafe_favicon.ico")