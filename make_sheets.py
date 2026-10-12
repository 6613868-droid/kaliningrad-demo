import os
from PIL import Image, ImageDraw

BASE = r"C:\Users\Алекс\.zcode\workspace\default\kaliningrad-demo\candidates"
for slug in ["hero", "ryb", "zel", "svet", "kosa", "balt"]:
    d = os.path.join(BASE, slug)
    files = sorted(f for f in os.listdir(d) if f.endswith(".jpg"))
    thumbs = []
    for f in files:
        im = Image.open(os.path.join(d, f)).convert("RGB")
        im.thumbnail((460, 340), Image.LANCZOS)
        thumbs.append((f, im))
    cols, rows = 2, (len(thumbs) + 1) // 2
    W, H = cols * 480 + 20, rows * 380 + 20
    sheet = Image.new("RGB", (W, H), (24, 24, 28))
    dr = ImageDraw.Draw(sheet)
    for i, (f, im) in enumerate(thumbs):
        x = 20 + (i % cols) * 480
        y = 20 + (i // cols) * 380
        sheet.paste(im, (x, y))
        dr.text((x + 6, y + 8), f.replace(".jpg", ""), fill=(255, 210, 140))
    sheet.save(os.path.join(BASE, f"sheet_{slug}.jpg"), "JPEG", quality=82)
    print(slug, sheet.size)
