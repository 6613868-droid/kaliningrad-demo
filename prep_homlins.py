import os
from PIL import Image

BASE = r"C:\Users\Алекс\.zcode\workspace\default\kaliningrad-demo"
IMG = os.path.join(BASE, "images")
HER = r"C:\Users\Алекс\Desktop\кейс 2\img"

# коллаж фигурок -> homlins.jpg
im = Image.open(os.path.join(HER, "photo_2023-05-25-11.17.00-1024x585 1.png")).convert("RGB")
im.save(os.path.join(IMG, "homlins.jpg"), "JPEG", quality=85, optimize=True)
print("homlins.jpg", im.size, os.path.getsize(os.path.join(IMG, "homlins.jpg")) // 1024, "KB")

# карта маршрута -> homlins-map.jpg (обрезаю вотермарку снизу)
im2 = Image.open(os.path.join(HER, "870_479_fixedwidth 1.png")).convert("RGB")
w, h = im2.size
im2 = im2.crop((0, 0, w, h - 32))
im2.save(os.path.join(IMG, "homlins-map.jpg"), "JPEG", quality=85, optimize=True)
print("homlins-map.jpg", im2.size, os.path.getsize(os.path.join(IMG, "homlins-map.jpg")) // 1024, "KB")
