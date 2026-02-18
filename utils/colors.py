import random

def generate_random_color():
    """Gera uma cor aleatória em hexadecimal com boa saturação"""
    colors = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#DDA0DD", "#20B2AA", "#FFB6C1", "#87CEEB", "#F08080",
        "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B88B",
        "#52C9D1", "#FF8B94", "#A8E6CF", "#FFD3B6", "#FFAAA5"
    ]
    return random.choice(colors)

def get_hover_color(base_color):
    """Gera uma cor de hover mais escura baseada na cor base"""
    # Converte hex para RGB
    hex_color = base_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Reduz a luminosidade em 20%
    r = max(0, int(r * 0.8))
    g = max(0, int(g * 0.8))
    b = max(0, int(b * 0.8))
    return f"#{r:02x}{g:02x}{b:02x}"
