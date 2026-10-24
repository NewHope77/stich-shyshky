"""Збирає гру: вставляє спрайти Стіча (WebP → base64) у game.html.

docs/index.html     — повна сторінка для GitHub Pages / iPad («На початковий екран» → на весь екран)
docs/artifact.html  — те саме без <!doctype>/<head> (для Artifact, обгортку додає платформа)
docs/manifest.webmanifest, docs/icon-*.png — іконка й повноекранний режим веб-застосунку
"""
import base64
import json
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).parent
dist = root.parent / "docs"
dist.mkdir(exist_ok=True)

html = (root / "game.html").read_text(encoding="utf-8")
for name in ("front", "left", "right", "happy"):
    b64 = base64.b64encode((root / "sprites" / f"{name}.webp").read_bytes()).decode()
    html = html.replace("{{%s}}" % name, "data:image/webp;base64," + b64)
assert "{{" not in html, "лишились незамінені спрайти"
(dist / "artifact.html").write_text(html, encoding="utf-8")

# іконка: Стіч на небі й травичці
def icon(size):
    im = Image.new("RGB", (size, size))
    d = ImageDraw.Draw(im)
    for y in range(size):
        t = y / size
        d.line([(0, y), (size, y)], fill=(int(118 + 120 * t), int(195 + 50 * t), int(239 - 20 * t)))
    d.rectangle([0, int(size * .72), size, size], fill=(122, 196, 88))
    st = Image.open(root / "cut" / "1.png").convert("RGBA")
    h = int(size * .78)
    st = st.resize((int(st.width * h / st.height), h), Image.LANCZOS)
    im.paste(st, ((size - st.width) // 2, int(size * .9) - h), st)
    return im

for s in (180, 192, 512):
    icon(s).save(dist / f"icon-{s}.png", optimize=True)

manifest = {
    "name": "Стіч і шишки", "short_name": "Стіч", "lang": "uk",
    "start_url": "./", "scope": "./", "display": "fullscreen", "orientation": "any",
    "background_color": "#9fd8f0", "theme_color": "#76c3ef",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
}
(dist / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

page = (
    '<!doctype html>\n<html lang="uk">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">\n'
    '<meta name="robots" content="noindex">\n'
    '<meta name="theme-color" content="#76c3ef">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
    '<meta name="apple-mobile-web-app-title" content="Стіч">\n'
    '<link rel="apple-touch-icon" href="icon-180.png">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    "<style>body{margin:0;font:14px system-ui,sans-serif}[hidden]{display:none!important}</style>\n"
    "</head>\n<body>\n" + html + "\n</body>\n</html>\n"
)
(dist / "index.html").write_text(page, encoding="utf-8")
print("index.html", len(page) // 1024, "KB, іконки й manifest готові")
