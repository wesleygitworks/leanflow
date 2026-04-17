# Arquivo: test_imagens.py
import os
from PIL import Image

def verificar_imagens():
    imagens_necessarias = [
        'lean_principle1.jpg', 'lean_principle2.jpg', 'lean_principle3.jpg',
        'lean_principle4.jpg', 'lean_principle5.jpg', 'lean_principle6.jpg', 
        'lean_principle7.jpg', 'kaizen.jpg', 'pdca.jpg', 'importancia_lean.jpg',
        'ferramentas_lean.jpg'
    ]
    
    print("Verificando imagens...")
    for imagem in imagens_necessarias:
        caminho = f"images/{imagem}"
        if os.path.exists(caminho):
            try:
                img = Image.open(caminho)
                print(f"✅ {imagem} - {img.size} - OK")
            except Exception as e:
                print(f"❌ {imagem} - ERRO: {str(e)}")
        else:
            print(f"❌ {imagem} - NÃO ENCONTRADA")

if __name__ == "__main__":
    verificar_imagens()