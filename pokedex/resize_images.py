import PIL
from PIL import Image
import os

dir_list = os.listdir("pokemon")
for i in dir_list:
    img = Image.open(f"pokemon/{i}")
    resize_img = img.resize((130, 130))
    resize_img.save(f"pokemon_resize/{i}")
