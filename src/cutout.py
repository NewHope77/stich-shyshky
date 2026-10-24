"""Вирізає Стіча з фото (rembg birefnet) → PNG з прозорим фоном, обрізаний по контуру."""
import sys
from pathlib import Path
from rembg import remove, new_session
from PIL import Image

src = Path(__file__).parent / "raw"
out = Path(__file__).parent / "cut"
out.mkdir(exist_ok=True)
session = new_session("birefnet-general-lite")
for name in sys.argv[1:]:
    im = Image.open(src / f"{name}.jpg").convert("RGB")
    cut = remove(im, session=session, post_process_mask=True)
    cut = cut.crop(cut.getbbox())
    cut.save(out / f"{name}.png")
    print(name, cut.size)
