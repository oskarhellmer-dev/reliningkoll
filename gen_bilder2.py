#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genererar om relining-foton via fal.ai Seedream v4 (fallback: OpenRouter).

Fokus: REALISM (dokumentärt, ospolat, halvt omskakad verklighet) — inte glossy stock.
Behåller 'ror-fore'. Gör om arbete, bil, utrustning + ror-efter (blå/rosa foder).

Sparar råa varianter i /tmp/relining_gen/ och en kontaktkarta att granska.
"""
import os, sys, json, time, base64, urllib.request
from io import BytesIO
from PIL import Image

RAW = "/tmp/relining_gen"
os.makedirs(RAW, exist_ok=True)
FAL = "https://fal.run/fal-ai/bytedance/seedream/v4/text-to-image"
OR = "https://openrouter.ai/api/v1/chat/completions"

STYLE = (", candid documentary photograph, real everyday Swedish setting, available light, "
         "slightly imperfect and unstyled, worn and lived-in, muted natural colours, "
         "shot on 35mm film, gentle grain, realistic, absolutely no text, no logo, no watermark, "
         "no brand names, no readable signage")

JOBS = [
 ("relining-arbete", "landscape_16_9",
  "Documentary photograph from behind and to the side: two workmen in orange high-visibility "
  "trousers with reflective stripes and dark t-shirts, one kneeling and feeding a thick blue "
  "flexible liner hose into an open cast-iron floor drain in a Swedish basement laundry room. "
  "A relining pump unit with a pressure gauge stands on the floor next to a part-used bucket of "
  "resin. Bare concrete floor, older painted walls, a water heater and copper pipes in the "
  "background, one work lamp giving uneven light. Mid-work, not posed."),
 ("relining-bil", "landscape_16_9",
  "Documentary photograph of a slightly dirty white work van parked on a gravel driveway beside "
  "an older Swedish house, its rear doors open. Inside the van: coiled blue hoses, a hose reel "
  "and relining equipment strapped to the walls. The bumper is mud-splashed, flat overcast "
  "autumn light, wet gravel. Unbranded plain van."),
 ("relining-utrustning", "landscape_4_3",
  "Documentary photograph of relining equipment set up on a bare concrete floor: a grey "
  "cylindrical pressure tank, a thick white insulated hose running from it along the skirting, "
  "a coiled blue hose with a shut-off valve, a small electric pump and a part-used resin bucket "
  "with its lid resting on top. Slight clutter, a work glove left on the floor, uneven daylight "
  "from a doorway."),
 ("ror-efter", "landscape_4_3",
  "Documentary close-up photograph looking straight down into a freshly relined drain pipe "
  "opening in a concrete floor. The interior is a smooth, seamless, glossy new lining in a "
  "vivid blue and pink colour, clean and even, filling the round opening."),
]

TARGET = {"relining-arbete": (1600, 900), "relining-bil": (1600, 900),
          "relining-utrustning": (1200, 900), "ror-efter": (1000, 750)}

def gen_fal(prompt, size, key, tries=3):
    body = json.dumps({"prompt": prompt + STYLE, "image_size": size, "num_images": 1}).encode()
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(FAL, data=body,
                headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=240))
            return urllib.request.urlopen(r["images"][0]["url"], timeout=120).read()
        except Exception as e:
            last = e; time.sleep(3)
    raise RuntimeError(f"fal: {last}")

def gen_or(prompt, key, tries=3):
    body = json.dumps({"model": "google/gemini-3.1-flash-image",
        "messages": [{"role": "user", "content": prompt + STYLE}],
        "modalities": ["image", "text"]}).encode()
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(OR, data=body,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=240))
            u = r["choices"][0]["message"]["images"][0]["image_url"]["url"]
            return base64.b64decode(u.split(",", 1)[1]) if u.startswith("data:") \
                   else urllib.request.urlopen(u, timeout=120).read()
        except Exception as e:
            last = e; time.sleep(4)
    raise RuntimeError(f"openrouter: {last}")

def crop_fill(im, tw, th):
    t = tw / th; w, h = im.size
    if w / h > t:
        nw = int(h * t); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = int(w / t); y = (h - nh) // 2; return im.crop((0, y, w, y + nh))

def main():
    fal = os.environ.get("FAL_KEY")
    orkey = os.environ.get("OPENROUTER_API_KEY")
    use = os.environ.get("GEN", "fal")
    if use == "fal" and not fal:
        use = "or"
    print("motor:", use)
    variants = int(os.environ.get("VARIANTS", "3"))
    only = [a for a in sys.argv[1:] if not a.isdigit()] or None
    montage = []
    for name, size, prompt in JOBS:
        if only and name not in only:
            continue
        for v in range(1, variants + 1):
            try:
                raw = gen_fal(prompt, size, fal) if use == "fal" else gen_or(prompt, orkey)
                im = Image.open(BytesIO(raw)).convert("RGB")
                tw, th = TARGET[name]
                im = crop_fill(im, tw, th).resize((tw, th), Image.LANCZOS)
                im.save(f"{RAW}/{name}-v{v}.jpg", "JPEG", quality=92)
                montage.append((f"{name} v{v}", im))
                print(f"OK   {name} v{v}")
            except Exception as e:
                print(f"ERR  {name} v{v}: {e}")
    if montage:
        cw, ch = 520, 325
        cols = 3
        card = Image.new("RGB", (cw * cols, ch * ((len(montage) + cols - 1) // cols)), (26, 30, 32))
        for i, (lab, im) in enumerate(montage):
            card.paste(crop_fill(im, cw, ch).resize((cw, ch), Image.LANCZOS),
                       ((i % cols) * cw, (i // cols) * ch))
        card.save("/tmp/relining_montage2.jpg", "JPEG", quality=90)
        print("montage -> /tmp/relining_montage2.jpg")
    print("KLART")

if __name__ == "__main__":
    main()
