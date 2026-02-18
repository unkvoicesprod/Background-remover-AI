from PIL import Image, ImageDraw, ImageFont
import os

def create_splash():
    """
    Gera um arquivo splash.png simples para testar a tela de carregamento.
    Usa as cores do tema do Soft BG Remover.
    """
    # Configurações de Tamanho e Cor
    width, height = 600, 350
    bg_color = "#0a0e27"     # Fundo Dark Blue (do tema)
    accent_color = "#00d4ff" # Ciano Neon
    text_color = "#ffffff"   # Branco
    
    # Criar imagem base
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Tentar carregar fontes (Arial é padrão no Windows)
    try:
        font_title = ImageFont.truetype("arial.ttf", 50)
        font_ver = ImageFont.truetype("arial.ttf", 24)
        font_load = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except IOError:
        # Fallback se não encontrar fonte
        font_title = ImageFont.load_default()
        font_ver = ImageFont.load_default()
        font_load = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Textos
    title = "Soft BG Remover"
    version = "Versão 2.0"
    loading = "Carregando Inteligência Artificial..."
    
    # Novos textos solicitados
    prog_text = "Programadores:  Francisco Armando Chico"
    year_text = "Ano de lançamento: 2026"
    dev_text = "Desenvolvida pela: SoftSafe.Company"

    # Função auxiliar para centralizar texto
    def draw_centered_text(text, font, y, color):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        draw.text((x, y), text, font=font, fill=color)

    # Desenhar Borda Neon
    draw.rectangle([(4, 4), (width-4, height-4)], outline=accent_color, width=2)
    
    # Desenhar Textos
    draw_centered_text(title, font_title, 70, accent_color)
    draw_centered_text(version, font_ver, 130, text_color)
    draw_centered_text(loading, font_load, 210, "#888888")

    # Desenhar Barra de Progresso (Visual)
    bar_width = 400
    bar_height = 8
    bar_x = (width - bar_width) / 2
    bar_y = 240
    # Fundo da barra
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], outline="#333333", width=1)

    # Desenhar Créditos no Splash
    draw_centered_text(prog_text, font_small, 270, "#aaaaaa")
    draw_centered_text(year_text, font_small, 290, "#aaaaaa")
    draw_centered_text(dev_text, font_small, 310, "#aaaaaa")

    # Salvar arquivo
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(base_dir, "splash.png")
    image.save(save_path)
    print(f"✅ Splash screen gerada com sucesso em: {save_path}")

if __name__ == "__main__":
    create_splash()