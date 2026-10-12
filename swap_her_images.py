import os
from PIL import Image

BASE = r"C:\Users\Алекс\.zcode\workspace\default\kaliningrad-demo"
IMG = os.path.join(BASE, "images")
HER = r"C:\Users\Алекс\Desktop\кейс 2\img"

# hero: закатный собор
im = Image.open(os.path.join(HER, "67_kaliningrad 1.png")).convert("RGB")
if im.width > 1600:
    im = im.resize((1600, int(im.height * 1600 / im.width)), Image.LANCZOS)
im.save(os.path.join(IMG, "hero.jpg"), "JPEG", quality=84, optimize=True)
print("hero.jpg", im.size, os.path.getsize(os.path.join(IMG, "hero.jpg")) // 1024, "KB")

# коса: лесная тропинка (карточка, с альфой как у остальных)
im2 = Image.open(os.path.join(HER, "фото 4.png")).convert("RGBA")
im2.save(os.path.join(IMG, "kosa.webp"), "WEBP", quality=86)
print("kosa.webp", im2.size, os.path.getsize(os.path.join(IMG, "kosa.webp")) // 1024, "KB")

# удалить неиспользуемый wikimedia-коса
old = os.path.join(IMG, "kosa.jpg")
if os.path.exists(old):
    os.remove(old)
    print("kosa.jpg removed")
