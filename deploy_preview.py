#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger en GitHub Pages-förhandsversion i mappen _preview (prefix /reliningkoll/)
och publicerar till gh-pages-grenen. main behåller produktionskoden."""
import os, re, shutil, subprocess, glob

ROOT = "/home/clawd/reliningkoll"
PREV = os.path.join(ROOT, "_preview")
PREFIX = "/reliningkoll"
GHBASE = "https://oskarhellmer-dev.github.io/reliningkoll"

if os.path.isdir(PREV):
    shutil.rmtree(PREV)
os.makedirs(PREV)

SKIP = {"_preview", ".git", ".hermes", ".impeccable", "__pycache__", "build_all.py", "build_core.py",
        "build_part1.py", "build_part2.py", "build_scale.py", "build_muni.py", "_check.py",
        "deploy_preview.py", "_deploy", "DESIGN.md", "PRODUCT.md"}

for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP]
    rel = os.path.relpath(root, ROOT)
    for fn in files:
        if fn in SKIP or fn.endswith(".py"):
            continue
        src = os.path.join(root, fn)
        dst_dir = os.path.join(PREV, rel) if rel != "." else PREV
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy2(src, os.path.join(dst_dir, fn))

# prefixa absoluta länkar i HTML
def fix_srcset(m):
    items = []
    for it in m.group(1).split(","):
        it = it.strip()
        if it.startswith("/"):
            it = PREFIX + it
        items.append(it)
    return 'srcset="' + ', '.join(items) + '"'

n_html = 0
for f in glob.glob(PREV + "/**/*.html", recursive=True):
    s = open(f, encoding="utf-8").read()
    s = re.sub(r'srcset="([^"]*)"', fix_srcset, s)
    s = s.replace('href="/', f'href="{PREFIX}/').replace('src="/', f'src="{PREFIX}/')
    # rätta dubbel-prefix om något redan prefixats
    s = s.replace(f'{PREFIX}{PREFIX}/', f'{PREFIX}/')
    open(f, "w", encoding="utf-8").write(s)
    n_html += 1

# CSS: fontvägar
for f in glob.glob(PREV + "/**/*.css", recursive=True):
    s = open(f, encoding="utf-8").read()
    s = s.replace("url(/fonts/", f"url({PREFIX}/fonts/")
    open(f, "w", encoding="utf-8").write(s)

# sitemap + robots för förhandsversionen
for f in [PREV + "/sitemap.xml", PREV + "/robots.txt"]:
    if os.path.exists(f):
        s = open(f, encoding="utf-8").read()
        s = s.replace("https://reliningkoll.se", GHBASE)
        open(f, "w", encoding="utf-8").write(s)

print("prefixade sidor:", n_html)
print("katalog:", PREV)
