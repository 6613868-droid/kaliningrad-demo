import os
from PIL import Image

IMG = r"C:\Users\Алекс\.zcode\workspace\default\kaliningrad-demo\images"
im = Image.open(os.path.join(IMG, "hero.jpg")).convert("RGB")
w, h = im.size
# кадр 1200x630 из центра верхней части (закат + собор)
target = 1200 / 630
cw = min(w, int(h * target))
ch = int(cw / target)
x0 = (w - cw) // 2
y0 = max(0, int(h * 0.18))
if y0 + ch > h:
    y0 = h - ch
im.crop((x0, y0, x0 + cw, y0 + ch)).resize((1200, 630), Image.LANCZOS).save(
    os.path.join(IMG, "og.jpg"), "JPEG", quality=84, optimize=True)
print("og.jpg", os.path.getsize(os.path.join(IMG, "og.jpg")) // 1024, "KB")
