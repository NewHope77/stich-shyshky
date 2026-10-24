"""Готує спрайти для гри: вирівнює яскравість нічних фото, зменшує, зберігає WebP."""
from pathlib import Path
from PIL import Image, ImageEnhance

cut = Path(__file__).parent / "cut"
out = Path(__file__).parent / "sprites"
out.mkdir(exist_ok=True)
H = 440
# назва → (файл, яскравість, насиченість)
plan = {
    "front": ("1", 1.04, 1.1),    # спереду (яскраве фото)
    "left":  ("4", 1.38, 1.15),   # дивиться вліво
    "right": ("6", 1.38, 1.15),   # дивиться вправо
    "happy": ("5", 1.3, 1.15),   # спереду, інший ракурс — для перемоги
}
for name, (src, bri, sat) in plan.items():
    im = Image.open(cut / f"{src}.png").convert("RGBA")
    rgb, a = im.convert("RGB"), im.getchannel("A")
    rgb = ImageEnhance.Brightness(rgb).enhance(bri)
    rgb = ImageEnhance.Color(rgb).enhance(sat)
    im = rgb.convert("RGBA"); im.putalpha(a)
    w = round(im.width * H / im.height)
    im = im.resize((w, H), Image.LANCZOS)
    p = out / f"{name}.webp"
    im.save(p, "WEBP", quality=86, method=6)
    print(name, im.size, p.stat().st_size // 1024, "KB")
