import time

class SmoothAnimator:
    """Classe para criar animações suaves em elementos da UI"""
    
    @staticmethod
    def fade_in(widget, duration=300, steps=20):
        """Efeito de fade in suave"""
        try:
            start_time = time.time()
            # initial_alpha = widget.cget("fg_color") if hasattr(widget, "cget") else None
            
            def animate():
                elapsed = (time.time() - start_time) * 1000
                progress = min(elapsed / duration, 1.0)
                
                # Atualizar opacidade (simulado via delay de renderização neste contexto)
                if progress < 1.0:
                    widget.after(int(duration / steps), animate)
            
            animate()
        except:
            pass
    
    @staticmethod
    def smooth_button_click(button, callback, original_color, hover_color):
        """Efeito de clique suave com feedback visual"""
        try:
            button.configure(fg_color=hover_color)
            button.after(50, lambda: button.configure(fg_color=original_color))
            button.after(60, callback)
        except:
            callback()
    
    @staticmethod
    def smooth_color_transition(widget, start_color, end_color, duration=300):
        """Transição suave entre cores"""
        try:
            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            def rgb_to_hex(rgb):
                return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'
            
            start_rgb = hex_to_rgb(start_color)
            end_rgb = hex_to_rgb(end_color)
            start_time = time.time()
            
            def animate():
                elapsed = (time.time() - start_time) * 1000
                progress = min(elapsed / duration, 1.0)
                current_rgb = tuple(int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * progress) for i in range(3))
                current_hex = rgb_to_hex(current_rgb)
                try: widget.configure(fg_color=current_hex)
                except: pass
                if progress < 1.0: widget.after(20, animate)
            animate()
        except: pass