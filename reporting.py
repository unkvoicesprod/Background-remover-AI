import logging
from logging.handlers import RotatingFileHandler
import platform
import socket
import uuid
import re
import psutil
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

LOG_FILENAME = 'app.log'
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 1

def setup_logging():
    try:
        handler = RotatingFileHandler(
            LOG_FILENAME,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    except Exception as e:
        print(f"Aviso: Não foi possível configurar o arquivo de log ({e}). O programa continuará sem logs.")

def get_system_info(app_version):
    """Coleta informações detalhadas do sistema para o relatório de erro."""
    try:
        info = {
            "Platform": platform.system(),
            "Platform Release": platform.release(),
            "Platform Version": platform.version(),
            "Architecture": platform.machine(),
            "Hostname": socket.gethostname(),
            "IP Address": socket.gethostbyname(socket.gethostname()),
            "MAC Address": ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            "Processor": platform.processor(),
            "RAM": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "App Version": app_version
        }
        return "\n".join([f"{k}: {v}" for k, v in info.items()])
    except Exception as e:
        logging.error(f"Erro ao coletar informações do sistema: {e}")
        return f"Não foi possível coletar informações do sistema: {e}"

def get_last_log_entry():
    """Lê e retorna a última entrada do arquivo de log."""
    try:
        log_path = os.path.join(os.getcwd(), LOG_FILENAME)
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    return lines[-1].strip()
    except Exception as e:
        return f"Erro ao ler log: {e}"
    return "Nenhum log encontrado."

def send_email_report(user_name, user_email, subject, body, app_version):
    """Envia o e-mail de relatório de erro usando SMTP."""
    recipient = "franciscoarmandochicogil@gmail.com"
    sender_email = "your_email@gmail.com"  # FIXME: PRECISA SER ALTERADO
    sender_password = "your_app_password"    # FIXME: PRECISA SER ALTERADO

    if sender_email == "your_email@gmail.com" or sender_password == "your_app_password":
        error_message = "Configuração Incompleta: O desenvolvedor não configurou o e-mail de envio."
        logging.error(error_message)
        print(error_message)
        return

    system_info = get_system_info(app_version)
    log_content = ""
    try:
        log_path = os.path.join(os.getcwd(), "app.log")
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                log_content = "".join(f.readlines()[-50:])
    except Exception as e:
        log_content = f"Erro ao ler log: {e}"

    full_body = f"Relatório de: {user_name} ({user_email})\nAssunto: {subject}\n\nDescrição:\n{'-'*20}\n{body}\n\nSistema:\n{'-'*20}\n{system_info}\n\nLogs:\n{'-'*20}\n{log_content}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = f"Relatório de Erro: {subject}"
    message.attach(MIMEText(full_body, "plain"))

    # ... (SMTP logic omitted for brevity, same as original)