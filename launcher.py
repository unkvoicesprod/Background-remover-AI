import tkinter as tk
from PIL import Image, ImageTk
import threading
import sys
import os
import time

# Variável global para armazenar a classe do App após importação
app_class = None

def main():
    # Tenta fechar o splash nativo do PyInstaller imediatamente
    try:
        import pyi_splash # type: ignore
        pyi_splash.close()
    except ImportError:
        pass

    # Configuração da Janela de Splash
    root = tk.Tk()
    root.overrideredirect(True) # Remove bordas da janela
    root.attributes("-topmost", True) # Mantém no topo
    
    # Dimensões (mesmas do create_splash.py)
    w, h = 600, 350
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    # Cor de fundo de segurança
    root.configure(bg="#0a0e27")

    # Carregar Imagem de Splash
    try:
        # Ajuste de caminho para funcionar tanto em dev quanto compilado
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_path, "splash.png")
        
        pil_img = Image.open(img_path)
        img = ImageTk.PhotoImage(pil_img)
        
        label = tk.Label(root, image=img, borderwidth=0, bg="#0a0e27")
        label.pack()
    except Exception as e:
        print(f"Erro ao carregar splash: {e}")
        tk.Label(root, text="Soft BG Remover\nCarregando...", bg="#0a0e27", fg="white", font=("Arial", 14)).pack(pady=100)

    # --- Barra de Progresso Dinâmica ---
    # Coordenadas baseadas no create_splash.py: 
    # Largura total 600. Barra largura 400. X inicial = (600-400)/2 = 100. Y = 240.
    bar_x = 100
    bar_y = 240
    bar_w = 400
    bar_h = 8
    accent_color = "#00d4ff"

    # Canvas para desenhar a barra sobre a imagem
    canvas = tk.Canvas(root, width=bar_w, height=bar_h, bg="#0a0e27", highlightthickness=0, bd=0)
    canvas.place(x=bar_x, y=bar_y)
    
    # Fundo da barra (para garantir contraste)
    canvas.create_rectangle(0, 0, bar_w, bar_h, fill="#0a0e27", outline="#333333")
    # A barra que vai crescer
    fill_rect = canvas.create_rectangle(0, 0, 0, bar_h, fill=accent_color, width=0)

    def update_bar(percent):
        """Atualiza a largura da barra baseada na porcentagem (0-100)"""
        width = (percent / 100) * bar_w
        canvas.coords(fill_rect, 0, 0, width, bar_h)
        root.update_idletasks()

    def load_application():
        """Função que roda em thread separada para importar o app pesado"""
        global app_class
        try:
            # Aqui acontece a mágica: importar o app carrega todas as bibliotecas pesadas
            import app
            app_class = app.YknarcsakEraserApp
        except Exception as e:
            print(f"Erro crítico ao carregar app: {e}")
            sys.exit(1)

    # Iniciar o carregamento em thread
    loader_thread = threading.Thread(target=load_application, daemon=True)
    loader_thread.start()

    # Loop de animação
    progress = 0
    while loader_thread.is_alive():
        # Simula progresso visual enquanto carrega
        if progress < 90:
            progress += 1 # Incremento lento
        
        update_bar(progress)
        root.update()
        time.sleep(0.03) # Controla a velocidade da animação

    # Finalizar carregamento (thread terminou)
    update_bar(100)
    time.sleep(0.2) # Pequena pausa para ver o 100%
    
    root.destroy() # Fecha splash

    # Inicia o App Principal
    if app_class:
        main_app = app_class()
        main_app.mainloop()

if __name__ == "__main__":
    main()