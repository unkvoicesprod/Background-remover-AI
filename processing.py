import os
import logging
from rembg import new_session, remove
from utils.paths import MODEL_PATH

def create_bg_session():
    if not os.path.exists(MODEL_PATH):
        # Se o modelo não estiver na pasta, o rembg tentará baixar
        return new_session("u2net")
    
    # Configura a variável de ambiente para forçar o rembg a usar o modelo local
    model_dir = os.path.dirname(MODEL_PATH)
    os.environ["U2NET_HOME"] = model_dir
    
    # Inicializa a sessão
    try:
        return new_session("u2net")
    except Exception as e:
        logging.error(f"Erro ao criar sessão rembg: {e}")
        print(f"Erro ao criar sessão rembg: {e}")
        return None