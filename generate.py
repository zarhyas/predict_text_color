import random
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def contrast(col1, col2):
  
    def get_luminance(color):
        color = [v / 255.0 for v in color]
        color = [((v / 12.92) if (v / 12.92) <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4) for v in color]
        return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]

    lum1 = get_luminance(col1)
    lum2 = get_luminance(col2)

    if lum1 > lum2:
        return (lum1 + 0.05) / (lum2 + 0.05)
    else:
        return (lum2 + 0.05) / (lum1 + 0.05)


def generer_exemples(n):
  
  folder_name = 'exemples'
  os.makedirs(folder_name, exist_ok=True)
  exemples = []
  
  for i in range(n):
    
      bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
      black_contrast = contrast(bg_color, (0, 0, 0))
      white_contrast = contrast(bg_color, (255, 255, 255))
      text_color = (0, 0, 0) if black_contrast > white_contrast else (255, 255, 255)
      
      img = Image.new('RGB', (500, 200), bg_color)
      d = ImageDraw.Draw(img)
      
      text = "Est-ce que c'est bien lisible?"
      font = ImageFont.truetype("arial.ttf", 25)
      textwidth, textheight = d.textsize(text, font)
      textx = (500 - textwidth) / 2
      texty = (200 - textheight) / 2
      d.text((textx, texty), text, fill=text_color, font=font)
      
      img.save(os.path.join(folder_name, f"exemple_{i}.png"))
        
      exemples.append((bg_color, text_color))

  return exemples

st.title("Générateur d'exemples")

n = st.slider("Nombre des exemples", 1, 1000, 100)

if st.button('Générer'):
  exemples = generer_exemples(n)
  st.subheader("Données d'entrainement")
  st.table(exemples)
  
  for i in range(n):
      st.image(f"exemples/exemple_{i}.png", caption=f"Exemple {i}")
