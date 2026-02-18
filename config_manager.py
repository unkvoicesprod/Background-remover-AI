import os
import json
import logging

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    default_config = {
        "app_name": "Soft BG Remover",
        "version": "2.0",
        "author": "SoftSafe",
        "license": "Freeware",
        "description": "Ferramenta offline de remoção de fundo com IA e editor integrado.",
        "website": "https://softsafecompany.github.io",
        "credits": "Desenvolvido por Yknarcsak.\nBaseado em U2NET e Rembg.\nProcessamento local e offline. \nCreditos para: softsafe.company@gmail.com\n\nProgramadores por Francisco Armando Chico\nAno de lançamento 2026\nDesenvolvida pela SoftSafe.Company",
        "sidebar_width": 250,
        "shortcuts": {
            "auto_remove": "b",
            "magic_erase": "m",
            "eraser": "e",
            "pencil": "p",
            "pan": "h",
            "rotate": "r",
            "fullscreen": "f"
        }
    }
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                default_config.update(json.load(f))
        except Exception as e:
            logging.error(f"Erro ao carregar config: {e}")
            print(f"Erro ao carregar config: {e}")
    return default_config

def save_config(config):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logging.error(f"Erro ao salvar config: {e}")
        print(f"Erro ao salvar config: {e}")

APP_CONFIG = load_config()
APP_NAME = APP_CONFIG["app_name"]
APP_VERSION = APP_CONFIG["version"]
APP_AUTHOR = APP_CONFIG["author"]
APP_LICENSE = APP_CONFIG["license"]
APP_DESCRIPTION = APP_CONFIG["description"]
APP_WEBSITE = APP_CONFIG["website"]
APP_CREDITS = APP_CONFIG["credits"]