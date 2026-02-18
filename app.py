import os
import threading
import logging
import webbrowser
import sys
from types import ModuleType
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog



from config_manager import APP_NAME, APP_VERSION, APP_AUTHOR, APP_WEBSITE, APP_DESCRIPTION, APP_LICENSE, APP_CREDITS
from reporting import setup_logging, send_email_report, LOG_FILENAME, get_system_info, get_last_log_entry
from processing import create_bg_session
from utils.paths import ICON_PATH
from utils.animator import SmoothAnimator
from ui.components.loading_spinner import LoadingSpinner
from ui.screens.home_screen import HomeScreen
from ui.screens.editor_screen import EditorInterface

# ==========================================
# INTERFACE GRÁFICA (GUI)
# ==========================================
class YknarcsakEraserApp(ctk.CTk): # type: ignore
    """Classe principal da aplicação que gerencia a janela e navegação."""
    def __init__(self):
        super().__init__()
        setup_logging()
        logging.info("Iniciando aplicação...")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.75) # Adjusted for smaller screens
        window_height = int(screen_height * 0.66)
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        
        self.title(f"{APP_NAME} v{APP_VERSION} | Dev: {APP_AUTHOR}")
        self.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#0a0e27")

        try:
            self.iconbitmap(ICON_PATH)
        except:
            pass

        self.session = None 
        # Iniciar carregamento da sessão em background automaticamente
        threading.Thread(target=self.init_session_background, daemon=True).start()

        self.spinner = LoadingSpinner(self, size=80, color="#E63946")
        
        # Menu superior (File, Edit, View, Configurações, Sobre) - REMOVED CTkMenuBar
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Abrir", command=self.open_manual_editor)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Sair", command=self.quit)
        self.menubar.add_cascade(label="Arquivo", menu=self.filemenu)
        
        self.configmenu = tk.Menu(self.menubar, tearoff=0)
        self.configmenu.add_command(label="Configurações", command=self.open_settings)
        self.configmenu.add_command(label="Logs", command=self.show_log_options)
        self.menubar.add_cascade(label="Ajuda", command=self.open_about_window)

        # Barra de Navegação Superior (Substituindo Sidebar)
        self.nav_bar = ctk.CTkFrame(self, height=50, corner_radius=0)
        self.nav_bar.pack(side="top", fill="x")
        
        self.btn_editor = ctk.CTkButton(self.nav_bar, text="Editar", command=self.open_manual_editor, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.config(menu=self.menubar)
        self.btn_editor.pack(side="left", padx=10, pady=10)

        # Container Principal
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.bind("<Configure>", self.on_window_resize)

        self.init_home_screen()
        
        # Tentar fechar splash screen após inicialização da interface
        self.after(200, self.close_splash)
    
    def close_splash(self):
        try:
            import pyi_splash # type: ignore
            if pyi_splash.is_alive():
                pyi_splash.close()
        except ImportError:
            pass
    
    def on_window_resize(self, event):
        pass #Fixed SyntaxError (corrected)

    def init_home_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.home_screen = HomeScreen(self.container, self)
        self.home_screen.pack(fill="both", expand=True)
    
    def open_settings(self):
        """Abre a janela de configurações."""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Configurações")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        settings_window.transient(self)
        settings_window.grab_set()
        settings_window.configure(fg_color="#0a0e27")

        settings_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (settings_window.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (settings_window.winfo_height() // 2)
        settings_window.geometry(f"+{x}+{y}")

        ctk.CTkLabel(settings_window, text="Configurações da Aplicação", font=("Roboto", 16, "bold"), text_color="#00d4ff").pack(pady=10)

        # Frame para opções de configuração
        options_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        options_frame.pack(padx=20, pady=10, fill="x")

        # # Opção para verificar permanentemente (REMOVED AS REQUESTED)
        # check_var = ctk.BooleanVar(value=True)
        # check_button = ctk.CTkCheckBox(options_frame, text="Verificar permanentemente", variable=check_var)
        # check_button.pack(pady=5, anchor="w")

        # Log Level Selection
        log_level_label = ctk.CTkLabel(options_frame, text="Nível de Log:", anchor="w")
        log_level_label.pack(fill="x")

        log_level_options = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        log_level_menu = ctk.CTkOptionMenu(options_frame, values=log_level_options, command=self.set_log_level)
        log_level_menu.pack(pady=5, anchor="w")

        def close_settings():
             settings_window.destroy()
        
        ctk.CTkButton(settings_window, text="Salvar e Fechar", command=close_settings, fg_color="#E63946", hover_color="#C0303A").pack(pady=10)

    def set_log_level(self, level):
        """Define o nível de log da aplicação."""
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            logging.error(f"Nível de log inválido: {level}")
            return

        logger = logging.getLogger()
        logger.setLevel(numeric_level)
        for handler in logger.handlers:
            handler.setLevel(numeric_level)

        logging.info(f"Nível de log alterado para: {level}")
        print(f"Nível de log alterado para: {level}")


    def show_log_options(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Gerenciar Logs")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        dialog.configure(fg_color="#0a0e27")
        
        ctk.CTkLabel(dialog, text="O que deseja fazer com o log?", font=("Roboto", 14), text_color="#ffffff").pack(pady=20)
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)
        
        def open_log():
            dialog.destroy()
            try:
                if os.path.exists("app.log"):
                    webbrowser.open(LOG_FILENAME)
                else:
                    messagebox.showinfo("Info", "Arquivo de log não encontrado.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o log: {e}")

        def clear_log_action():
            dialog.destroy()
            self.clear_logs()

        ctk.CTkButton(btn_frame, text="📂 Abrir", command=open_log, width=100, fg_color="#178FBE", hover_color="#051C25").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Limpar", command=clear_log_action, fg_color="#A52731", hover_color="#240608", width=100).pack(side="right", padx=5)

    def clear_logs(self):
        if messagebox.askyesno("Limpar Logs", "Tem certeza que deseja apagar todo o histórico de logs?"):
            try:
                logger = logging.getLogger()
                for handler in logger.handlers[:]:
                    if isinstance(handler, logging.FileHandler): 
                        handler.close()
                        logger.removeHandler(handler)
                with open("app.log", 'w', encoding='utf-8'): pass
                setup_logging()
                logging.info("Logs limpos pelo usuário.")
                messagebox.showinfo("Sucesso", "Arquivo de log limpo com sucesso!")
            except Exception as e:
                logging.error(f"Erro ao limpar logs: {e}")
                messagebox.showerror("Erro", f"Não foi possível limpar os logs: {e}")

    def open_report_window(self):
        """Abre uma janela para o usuário preencher e enviar um relatório de erro."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Reportar Erro")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color="#0a0e27")

        ctk.CTkLabel(dialog, text="Relatório de Erro", font=("Roboto", 20, "bold"), text_color="#00d4ff").pack(pady=(15, 10))

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=20, pady=10, fill="x")

        # Campos do formulário
        ctk.CTkLabel(form_frame, text="Seu Nome Completo:", anchor="w").pack(fill="x")
        name_entry = ctk.CTkEntry(form_frame, placeholder_text="Seu nome")
        name_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Seu E-mail:", anchor="w").pack(fill="x")
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="seu.email@exemplo.com")
        email_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Assunto:", anchor="w").pack(fill="x")
        subject_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: O programa fechou inesperadamente")
        subject_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form_frame, text="Descrição Detalhada do Erro:", anchor="w").pack(fill="x")
        body_textbox = ctk.CTkTextbox(form_frame, height=200, scrollbar_button_color="#1f294f", scrollbar_button_hover_color="#00d4ff")
        body_textbox.pack(fill="x", expand=True, pady=(0, 20))

        # Preencher automaticamente com informações do sistema e último log
        system_info = get_system_info(APP_VERSION)
        last_log = get_last_log_entry()

        pre_filled_text = (
            f"Por favor, descreva o que aconteceu acima desta linha.\n\n"
            f"{'='*40}\n"
            f"INFORMAÇÕES DO DISPOSITIVO (COLETADO AUTOMATICAMENTE)\n"
            f"{'='*40}\n"
            f"{system_info}\n\n"
            f"{'='*40}\n"
            f"ÚLTIMO LOG REGISTRADO\n"
            f"{'='*40}\n"
            f"{last_log}\n"
        )
        body_textbox.insert("0.0", pre_filled_text)

        def on_send():
            # Validação simples
            if not all([name_entry.get(), email_entry.get(), subject_entry.get(), body_textbox.get("1.0", "end-1c")]):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.", parent=dialog)
                return
            
            # Iniciar envio em uma nova thread para não travar a UI
            threading.Thread(target=send_email_report, args=(
                name_entry.get(),
                email_entry.get(),
                subject_entry.get(),
                body_textbox.get("1.0", "end-1c"),
                dialog,
                APP_VERSION
            ), daemon=True).start()

        # Botão de Envio
        send_button = ctk.CTkButton(dialog, text="Enviar Relatório", command=on_send, fg_color="#2ECC71", hover_color="#1E8449")
        send_button.pack(pady=10)

    def report_error(self):
        """Abre a janela de relatório de erros."""
        self.open_report_window()

    def open_about_window(self):
        """Abre a janela 'Sobre'."""
        about_window = ctk.CTkToplevel(self)
        about_window.title("Sobre")
        about_window.geometry("500x420")
        about_window.resizable(False, False)
        about_window.transient(self)
        about_window.grab_set()
        about_window.configure(fg_color="#0a0e27")
        
        ctk.CTkLabel(about_window, text=str(APP_NAME), font=("Roboto", 20, "bold"), text_color="#26dbff").pack(pady=(25, 5))
        ctk.CTkLabel(about_window, text=APP_DESCRIPTION, font=("Roboto", 11, "italic"), text_color="#a0a0a0").pack(pady=(0, 5))
        ctk.CTkLabel(about_window, text=f"Versão: {APP_VERSION}", font=("Roboto", 12), text_color="#e1e2e3").pack(pady=2)
        ctk.CTkLabel(about_window, text=f"Autor: {APP_AUTHOR}", font=("Roboto", 12), text_color="#e1e2e3").pack(pady=2)
        ctk.CTkLabel(about_window, text=f"Licença: {APP_LICENSE}", font=("Roboto", 12), text_color="#e1e2e3").pack(pady=2)
        
        if APP_WEBSITE:
            link = ctk.CTkLabel(about_window, text=APP_WEBSITE, font=("Roboto", 12, "bold","underline"), text_color="#00d4ff", cursor="hand2")
            link.pack(pady=2)
            link.bind("<Button-1>", lambda e: webbrowser.open(APP_WEBSITE))
        
        textbox = ctk.CTkTextbox(about_window, width=320, height=120, fg_color="#1a1f3a", text_color="#e1e2e3", scrollbar_button_color="#1f294f", scrollbar_button_hover_color="#00d4ff")
        textbox.pack(pady=15)
        textbox.insert("0.0", APP_CREDITS)
        textbox.configure(state="disabled")
        
        ctk.CTkButton(about_window, text="Fechar", command=about_window.destroy, fg_color="#E63946", hover_color="#C0303A").pack(pady=10)

    def open_manual_editor(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(
                title="Selecione uma imagem para editar",
                filetypes=[("Imagens", "*.jpg *.jpeg *.png *.webp")]
            )
        if file_path:
            for widget in self.container.winfo_children():
                def fade_out(w):
                    try: w.pack_forget()
                    except: pass
                widget.after(50, lambda w=widget: fade_out(w))
            
            def create_editor():
                editor_instance = EditorInterface(self.container, file_path, self.session, self.init_home_screen)
                editor_instance.pack(fill="both", expand=True)
                SmoothAnimator.fade_in(editor_instance, duration=300)
            
            self.after(100, create_editor)

    def init_session_background(self):
        """Inicializa a sessão de remoção de fundo em uma thread separada."""
        try:
            self.session = create_bg_session()
        except Exception as e:
            logging.error(f"Falha ao iniciar sessão em background: {e}")

if __name__ == "__main__":
    try:
        app = YknarcsakEraserApp()
        app.mainloop()
    except Exception as e:
        logging.error(f"Erro fatal na inicialização: {e}")
        print(f"Erro fatal na inicialização: {e}")
        raise