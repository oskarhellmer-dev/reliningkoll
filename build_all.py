#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, glob, json
sys.path.insert(0, "/home/clawd/reliningkoll")
import build_core as C
from build_core import write, BASE, ROOT
import build_muni as M
import build_part1 as P1
import build_part2 as P2
import build_scale as S
import build_geo as GE
import build_guides2 as G2

# ---- injicera skalning
P1.CITIES = [t for t in M.ALL if t[0] in GE.GEO]      # behåll för ev. referens
P2.CITIES = M.ALL
P1.GUIDES.update(S.NEW_GUIDES)
P1.GUIDES.update(G2.G)
P2.PRICES.update(S.NEW_PRICES)
P2.FIRMS = P2.FIRMS + S.NEW_FIRMS

# 1. bygg alla sidor
C.build_home()
P1.build_guides()
P2.build_prices()
GE.build_cities_geo()      # data-drivna kommunsidor (60 st, riktig SCB-data)
P2.build_firms()
GE.build_service_geo()     # data-drivna tjänsteorter (24 st)
P2.build_pages()

# 2. injicera kommun-länkar i startsidan (endast kuraterade orter)
idx = os.path.join(ROOT, "index.html")
html = open(idx, encoding="utf-8").read()
pills = ''.join(f'<a href="/relining/{s}/">{GE.GEO[s]["name"]}</a>' for s in GE.CITY_SET)
html = html.replace('<div class="pills rv" id="city-pills"></div>',
                    f'<div class="pills rv">{pills}<a href="/relining/"><strong>Alla kommuner</strong></a></div>')
open(idx, "w", encoding="utf-8").write(html)
print("  startsidan: kommun-länkar injicerade")

# 3. robots.txt (AI-crawlers tillåtna)
robots = """User-agent: *
Allow: /

# AI-crawlers tillåtna med samma regler.
User-agent: GPTBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: PerplexityBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: Meta-ExternalAgent
User-agent: cohere-ai
Allow: /

Sitemap: https://reliningkoll.se/sitemap.xml
"""
write("/robots.txt", robots)

# 4. sitemap.xml
urls = []
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    rel = f.replace(ROOT, "")
    if rel.endswith("404.html"):
        continue
    if rel.startswith("/_preview/") or rel.startswith("/__pycache__/"):
        continue
    if rel.endswith("index.html"):
        rel = rel[:-len("index.html")]
    loc = BASE + rel
    if not loc.endswith("/") and "." not in rel.split("/")[-1]:
        loc += "/"
    if loc == BASE + "/index.html":
        loc = BASE + "/"
    urls.append(loc)
urls = sorted(set(urls))
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    pr = "1.0" if u == BASE + "/" else ("0.8" if u.count("/") <= 4 else "0.6")
    sm.append(f"  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>")
sm.append("</urlset>")
write("/sitemap.xml", "\n".join(sm))
print(f"  sitemap: {len(urls)} URL:er")

# 4b. llms.txt (AEO)
llms = """# Reliningkoll

> Oberoende jämförelsetjänst för relining, avloppsspolning och rörinspektion i Sverige.
> Besökaren beskriver sitt ärende en gång och matchas med upp till tre granskade lokala
> entreprenörer. Kostnadsfritt för privatpersoner, ingen bindningstid.

## Om tjänsten

- Tjänst: kostnadsfri offertförmedling för relining, avloppsspolning och rörinspektion.
- Målgrupp: svenska fastighetsägare, villaägare och bostadsrättsföreningar med äldre avloppsrör.
- Intäkt: anslutna firmor betalar per förfrågan de accepterar. Besökaren betalar inget.
- Kontakt: hej@reliningkoll.se

## Viktiga sidor

- [Priser 2026](/pris/): riktpriser för relining, villa, bostadsrätt, per meter, spolning och rörinspektion.
- [Guider](/guider/): metoder, livslängd, gjutjärnsrör, ROT-avdrag, val av firma och fallgropar.
- [Relining i din kommun](/relining/): lokalt bostadsbestånd och byggnadsperioder per kommun (källa: SCB).
- [Avloppsspolning](/avloppsspolning/) och [rörinspektion](/rorinspektion/) per ort.
- [För proffs](/for-proffs/): för entreprenörer som vill ta emot leads.
- [Om oss](/om-oss/): hur tjänsten och granskningen fungerar.

## Fakta

- Relining förnyar avloppsrör inifrån utan rivning. Livslängd normalt 40 till 50 år.
- Hus byggda fram till omkring 1970 har i regel gjutjärnsrör; därefter blev plaströr vanligare.
- ROT-avdrag ger 30 procent av arbetskostnaden tillbaka i egen villa, tak 50 000 kr per person och år.
- All kommunstatistik på sajten kommer från SCB:s öppna API. Vi publicerar inga påhittade betyg eller recensioner.
"""
write("/llms.txt", llms)
print("  llms.txt skriven")

# 5. favicon.svg
fav = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#08312f"/>
<path d="M32 12c9 10.2 15 18.6 15 26.4A15 15 0 0 1 17 38.4C17 30.6 23 22.2 32 12Z" fill="#12897f"/>
<path d="M25 37.5a7.5 7.5 0 0 0 7.5 7.5" stroke="#eaf5f3" stroke-width="3.4" stroke-linecap="round" fill="none"/>
</svg>'''
write("/favicon.svg", fav)

# 6. PNG-bilder via Pillow
from PIL import Image, ImageDraw, ImageFont
def font(sz, bold=True):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

def icon(size):
    im = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(im)
    r = int(size*0.22)
    d.rounded_rectangle([0,0,size-1,size-1], radius=r, fill=(8,49,47,255))
    s = size/64
    cx = size/2
    top = 12*s; bot = 38.4*s
    d.polygon([(cx,top),(cx+15*s,38.4*s),(cx+11*s,44*s),(cx-11*s,44*s),(cx-15*s,38.4*s)], fill=(18,137,127,255))
    d.arc([cx-7.5*s, 30*s, cx+7.5*s, 45*s], 0, 90, fill=(234,245,243,255), width=max(2,int(3.4*s)))
    return im

for name, size in [("favicon-32.png",32),("apple-touch-icon.png",180)]:
    icon(size).save(os.path.join(ROOT, name))
    print("  bild:", name)

# og.png 1200x630
W,H = 1200,630
og = Image.new("RGB",(W,H),(8,49,47))
d = ImageDraw.Draw(og)
d.rectangle([0,H-190,W,H], fill=(6,40,38))
d.polygon([(96,120),(96+120,300),(96+88,352),(96-88,352)], fill=(18,137,127))
d.arc([96-60,238,96+60,352],0,90,fill=(234,245,243),width=14)
d.text((96,392), "Reliningkoll", font=font(72,True), fill=(255,255,255))
d.text((96,478), "Jämför relining och avloppsrenovering", font=font(34,False), fill=(184,210,206))
d.text((96,530), "Upp till 3 offerter från lokala firmor. Gratis.", font=font(30,False), fill=(143,216,207))
og.save(os.path.join(ROOT,"og.png"))
print("  bild: og.png")

# 7. summering
n = len([f for f in glob.glob(os.path.join(ROOT,"**","*.html"), recursive=True)
         if "/_preview/" not in f and "/__pycache__/" not in f])
print(f"\nKLART: {n} HTML-sidor, sitemap {len(urls)}, robots, favicon (svg/png), og.png")
