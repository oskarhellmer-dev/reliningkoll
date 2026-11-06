#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mäter hur lika kommunsidorna är varandra. Riktig evidens, inte gissning."""
import os, re, glob, itertools, random
from collections import Counter

ROOT = "/home/clawd/reliningkoll"

def maintext(path):
    h = open(path, encoding="utf-8").read()
    m = re.search(r'<main id="main">(.*?)</main>', h, re.S)
    body = m.group(1) if m else h
    body = re.sub(r'<script.*?</script>', ' ', body, flags=re.S)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'&[a-z]+;', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    return body

def shingles(text, n=5):
    w = text.split()
    return set(tuple(w[i:i+n]) for i in range(len(w)-n+1))

def normalize(text):
    # ta bort stadsnamn så vi jämför innehållet, inte namnet
    return text

pages = {}
for f in glob.glob(ROOT + "/relining/*/index.html"):
    slug = f.split("/relining/")[1].split("/")[0]
    pages[slug] = maintext(f)

print(f"Kommunsidor: {len(pages)}")
wc = [len(t.split()) for t in pages.values()]
print(f"Ord per sida (main): min {min(wc)}, median {sorted(wc)[len(wc)//2]}, max {max(wc)}")

# 1. Gemensamma shingles över ALLA sidor = boilerplate
sh = {s: shingles(t) for s, t in pages.items()}
common = set.intersection(*sh.values()) if sh else set()
print(f"\nOrdsekvenser (5-ord) som finns i ALLA 290 sidor: {len(common)}")
# hur stor andel av en typisk sida är exakt denna gemensamma text?
sample = list(pages)[0]
total_sh = len(sh[sample])
print(f"Andel av en typisk kommunsida som är ORDAGRANT identisk med alla andra: "
      f"{100*len(common)/total_sh:.1f}%")

# 2. Genomsnittlig pairwise Jaccard på slumpat urval
random.seed(1)
keys = random.sample(list(pages), 60)
sims = []
for a, b in itertools.combinations(keys, 2):
    sa, sb = sh[a], sh[b]
    j = len(sa & sb) / len(sa | sb)
    sims.append(j)
sims.sort()
print(f"\nParvis likhet (Jaccard, 5-ord) över {len(sims)} par:")
print(f"  median {sims[len(sims)//2]*100:.1f}%  |  min {sims[0]*100:.1f}%  |  max {sims[-1]*100:.1f}%")
print(f"  andel par över 70% likhet: {100*sum(1 for s in sims if s>0.70)/len(sims):.1f}%")
print(f"  andel par över 85% likhet: {100*sum(1 for s in sims if s>0.85)/len(sims):.1f}%")

# 3. Unikt innehåll per sida = shingles som bara finns på den sidan
uniq = []
for s in pages:
    others = set()
    for o in pages:
        if o != s: others |= sh[o]
    uniq.append(len(sh[s] - others))
print(f"\nUnika ordsekvenser per sida: median {sorted(uniq)[len(uniq)//2]}, "
      f"min {min(uniq)}, max {max(uniq)}")
print(f"  sidor med <5 unika sekvenser: {sum(1 for u in uniq if u<5)} av {len(uniq)}")

# 4. Titel/meta-diff: hur många unika ord i titlarna
titles = []
for s in pages:
    h = open(ROOT+f"/relining/{s}/index.html", encoding="utf-8").read()
    t = re.search(r'<title>(.*?)</title>', h).group(1)
    titles.append(t)
# ta bort stadsnamn -> hur många distinkta titelmönster kvar?
pat = Counter()
for s, t in zip(pages, titles):
    name = None
    pat[re.sub(r'\b\w+\b', 'X', t)] += 1
print(f"\nDistinkta titelmönster när man byter ut ord mot X: {len(pat)}")
for k, v in pat.most_common(3):
    print(f"   x{v}: {k}")
