from PIL import Image, ImageDraw, ImageFont
import os

def criar_imagem_placeholder(nome_arquivo, texto):
    """Cria uma imagem placeholder com texto"""
    img = Image.new('RGB', (500, 350), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Tente carregar uma fonte, use padrão se não disponível
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # Centralizar texto
    bbox = draw.textbbox((0, 0), texto, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (500 - text_width) // 2
    y = (350 - text_height) // 2
    
    draw.text((x, y), texto, fill='black', font=font)
    img.save(f"images/{nome_arquivo}")
    print(f"✅ Criada imagem placeholder: {nome_arquivo}")

# Criar pasta images se não existir
if not os.path.exists('images'):
    os.makedirs('images')

# Criar imagens faltantes
imagens_faltantes = {
    'lean_principle1.jpg': 'Princípio 1:\nEliminar Desperdícios',
    'lean_principle6.jpg': 'Princípio 6:\nQualidade na Fonte', 
    'lean_principle7.jpg': 'Princípio 7:\nRespeito às Pessoas',
    'ferramentas_lean.jpg': 'Ferramentas\nLean'
}

for arquivo, texto in imagens_faltantes.items():
    if not os.path.exists(f'images/{arquivo}'):
        criar_imagem_placeholder(arquivo, texto)

print("✅ Todas as imagens necessárias estão disponíveis!")