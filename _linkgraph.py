#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Länkgraf-analys: nåbarhet, orphans, djup, in/ut-länkar."""
import os, re, glob, collections

ROOT = "/home/clawd/reliningkoll"
pages = {}
for f in glob.glob(ROOT + "/**/*.html", recursive=True):
    if "/_preview/" in f or "/.hermes/" in f: continue
    rel = f.replace(ROOT, "")
    if rel.endswith("404.html"): continue
    pages[rel] = open(f, encoding="utf-8", errors="ignore").read()

def norm(p):
    if p.endswith("/index.html"): return p[:-len("index.html")]
    return p

def resolve(u):
    """intern absolut lank -> normaliserad sidnyckel"""
    u = u.split("#")[0].split("?")[0]
    if not u.startswith("/"): return None
    if u == "/": return "/index.html"
    if u.endswith("/"): return u + "index.html"
    if "." in u.split("/")[-1]: return u
    return u + "/index.html"

out = {}
inn = collections.defaultdict(set)
for rel, h in pages.items():
    tgts = set()
    for m in re.findall(r'<a\s[^>]*href="(/[^"#?]*)"', h):
        k = resolve(m)
        if k and k in pages: tgts.add(k)
    out[rel] = tgts
    for t in tgts: inn[t].add(rel)

home = "/index.html"
# BFS-djup
depth = {home: 0}
q = collections.deque([home])
while q:
    cur = q.popleft()
    for t in out.get(cur, ()):
        if t not in depth:
            depth[t] = depth[cur] + 1
            q.append(t)

orphans = [p for p in pages if p not in depth]
no_out = [p for p in pages if not out.get(p)]
deep = sorted([(d, p) for p, d in depth.items() if d >= 4], reverse=True)
zero_in = sorted([p for p in pages if len(inn[p]) == 0 and p != home])

print(f"Sidor: {len(pages)}")
print(f"Nåbara från startsidan: {len(depth)}")
print(f"ORPHANS (ej nåbara): {len(orphans)}")
for p in orphans[:20]: print("   ", p)
print(f"Max klickdjup: {max(depth.values()) if depth else 0}")
print(f"Sidor på djup >=4: {len(deep)}")
for d, p in deep[:15]: print(f"    {d}  {p}")
print(f"\nSidor utan UTGÅENDE interna länkar: {len(no_out)}")
for p in no_out[:15]: print("   ", p)
print(f"\nSidor med 0 inkommande interna länkar (utom startsidan): {len(zero_in)}")
for p in zero_in[:15]: print("   ", p)

# inlänkar per sida - lägst först
low = sorted((len(inn[p]), p) for p in pages if p != home)[:12]
print("\nFärst inkommande länkar:")
for n, p in low: print(f"    {n:3d}  {p}")

# genomsnitt ut
avg = sum(len(v) for v in out.values()) / max(len(out), 1)
print(f"\nSnitt utgående interna länkar/sida: {avg:.1f}")
