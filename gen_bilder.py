#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genererar dokumentära relining-foton via OpenRouter (Google Gemini image).

Samma budskap som Oskars referensbilder (arbete, utrustning, före/efter-rör)
men INTE kopior: inga logotyper, inga företagsnamn, ingen text i bilden.
Stil: dokumentär, kandid, ospolad — passar "besiktningsprotokollet".
"""
import os, sys, json, time, base64, urllib.request
from io import BytesIO
from PIL import Image

OUT = "/home/clawd/reliningkoll/bilder"
os.makedirs(OUT, exist_ok=True)
MODEL = os.environ.get("IMG_MODEL", "google/gemini-3.1-flash-image")

STYLE = (", candid documentary photograph, real everyday Swedish setting, available light, "
         "slightly imperfect and unstyled, muted natural colours, shot on 35mm film, gentle grain, "
         "realistic, absolutely no text, no logo, no watermark, no brand names, no readable signage")

JOBS = [
 ("relining-arbete",
  "Two relining technicians in orange high-visibility workwear with reflective silver stripes and "
  "white safety helmets, kneeling beside an open floor drain in a residential basement. One feeds a "
  "flexible blue liner hose into a cast-iron drain pipe while the other operates a small blue relining "
  "pump unit with a pressure gauge on the concrete floor. Bare concrete floor, plain painted walls, a "
  "wooden door in the background, one work light."),
 ("relining-bil",
  "A plain unbranded white service van parked on an ordinary Swedish residential street, its rear doors "
  "open showing neatly coiled blue hoses and relining equipment on shelves inside. Two workers in dark "
  "work jackets seen from behind walking toward the van. Overcast daylight, ordinary suburban houses."),
 ("relining-utrustning",
  "Relining equipment set up on a bare concrete floor: a grey cylindrical resin mixing container with a "
  "metal fitting on top, a white insulated hose connected and running along a plain wall, a tidy coil of "
  "blue hose beside it and a small pump unit."),
 ("ror-fore",
  "Close-up documentary photograph looking straight down into an old cast-iron drain pipe opening in a "
  "concrete floor. The interior is heavily corroded, rough and rust-orange with scale and mineral buildup."),
 ("ror-efter",
  "Close-up documentary photograph looking straight down into a relined drain pipe opening in a concrete "
  "floor. The interior is smooth, seamless and even, coated in a pale grey-beige epoxy lining, clean and "
  "uniform."),
]

TARGET = {
 "relining-arbete": (1600, 900), "relining-bil": (1600, 900),
 "relining-utrustning": (1200, 900), "ror-fore": (1000, 750), "ror-efter": (1000, 750),
}

def gen(prompt, key, tries=3):
    body = json.dumps({"model": MODEL,
        "messages": [{"role": "user", "content": prompt + STYLE}],
        "modalities": ["image", "text"]}).encode()
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
                data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=240))
            imgs = r["choices"][0]["message"].get("images") or []
            if not imgs:
                raise RuntimeError("inga bilder i svar")
            return imgs[0]["image_url"]["url"]
        except Exception as e:
            last = e; time.sleep(4)
    raise RuntimeError(f"misslyckades: {last}")

def crop_fill(im, tw, th):
    t = tw / th; w, h = im.size
    if w / h > t:
        nw = int(h * t); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = int(w / t); y = (h - nh) // 2; return im.crop((0, y, w, y + nh))

def save(name, raw, variant=""):
    im = Image.open(BytesIO(raw)).convert("RGB")
    tw, th = TARGET[name]
    im = crop_fill(im, tw, th).resize((tw, th), Image.LANCZOS)
    suffix = f"-v{variant}" if variant else ""
    for wpx in (tw, tw // 2):
        px = im.resize((wpx, int(th * wpx / tw)), Image.LANCZOS)
        px.save(f"{OUT}/{name}{suffix}-{wpx}.webp", "WEBP", quality=82, method=6)
    im.save(f"{OUT}/{name}{suffix}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    return im

def main():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("Sätt OPENROUTER_API_KEY"); sys.exit(1)
    variants = int(os.environ.get("VARIANTS", "1"))
    only = [a for a in sys.argv[1:] if not a.isdigit()] or None
    montage = []
    for name, prompt in JOBS:
        if only and name not in only:
            continue
        for v in range(1, variants + 1):
            try:
                url = gen(prompt, key)
                raw = base64.b64decode(url.split(",", 1)[1]) if url.startswith("data:") \
                      else urllib.request.urlopen(url, timeout=120).read()
                im = save(name, raw, v if variants > 1 else "")
                montage.append((f"{name} v{v}", im))
                print(f"OK   {name} v{v}")
            except Exception as e:
                print(f"ERR  {name} v{v}: {e}")
    if montage and os.environ.get("MONTAGE", "1") == "1":
        cw, ch = 480, 300
        card = Image.new("RGB", (cw * 3, ch * ((len(montage) + 2) // 3)), (30, 34, 36))
        for i, (label, im) in enumerate(montage):
            thumb = crop_fill(im, cw, ch).resize((cw, ch), Image.LANCZOS)
            card.paste(thumb, ((i % 3) * cw, (i // 3) * ch))
        card.save("/tmp/relining_montage.jpg", "JPEG", quality=88)
        print("montage -> /tmp/relining_montage.jpg", [m[0] for m in montage])
    print("KLART")

if __name__ == "__main__":
    main()
