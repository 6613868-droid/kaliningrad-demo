import os
from PIL import Image

BASE = r"C:\Users\Алекс\.zcode\workspace\default\kaliningrad-demo"
C = os.path.join(BASE, "candidates")
IMG = os.path.join(BASE, "images")
HER = r"C:\Users\Алекс\Desktop\кейс 2\img"
os.makedirs(IMG, exist_ok=True)

# Фото Александры (PNG со скруглёнными углами -> WebP с альфой)
her = {
    "knr.webp":  "фото 1.png",   # Рыбная деревня, маяк
    "zel.webp":  "фото2.png",    # Зеленоградск с высоты
    "svet.webp": "фото3.png",    # Светлогорск, башня на закате
    "balt.webp": "фото5.png",    # побережье/коса с высоты -> Балтийск
}
for dst, src in her.items():
    im = Image.open(os.path.join(HER, src)).convert("RGBA")
    im.save(os.path.join(IMG, dst), "WEBP", quality=86)
    print(dst, im.size, os.path.getsize(os.path.join(IMG, dst)) // 1024, "KB")

# Wikimedia-заглушки (пока нет своих: hero-закат и лесная коса)
wm = {
    "hero.jpg": "hero/hero_4.jpg",
    "kosa.jpg": "kosa/kosa_1.jpg",
}
for dst, src in wm.items():
    im = Image.open(os.path.join(C, src)).convert("RGB")
    if im.width > 1600:
        im = im.resize((1600, int(im.height * 1600 / im.width)), Image.LANCZOS)
    im.save(os.path.join(IMG, dst), "JPEG", quality=82, optimize=True)
    print(dst, im.size, os.path.getsize(os.path.join(IMG, dst)) // 1024, "KB")
