#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stenhård granskning av reliningkoll.se:s byggda filer."""
import os, re, glob, json, collections, html as H

ROOT = "/home/clawd/reliningkoll"
BASE = "https://reliningkoll.se"

pages = {}
for f in glob.glob(ROOT + "/**/*.html", recursive=True):
    if "/_preview/" in f or "/.hermes/" in f:
        continue
    rel = f.replace(ROOT, "")
    pages[rel] = open(f, encoding="utf-8", errors="ignore").read()

def url_of(rel):
    if rel.endswith("/index.html"):
        return rel[:-len("index.html")]
    return rel

def exists(path):
    if not path.startswith("/"): return True
    p = ROOT + path.split("#")[0].split("?")[0]
    if p.endswith("/"): p += "index.html"
    if os.path.isfile(p): return True
    if os.path.isfile(p + "/index.html"): return True
    return False

issues = collections.defaultdict(list)
def flag(kind, rel, detail=""):
    issues[kind].append((rel, detail))

titles = collections.Counter()
metas = collections.Counter()
h1s = collections.Counter()

links_out = collections.defaultdict(set)   # rel -> set of target paths
links_in = collections.defaultdict(set)

for rel, h in pages.items():
    if rel.endswith("404.html"):
        continue
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    title = H.unescape(t.group(1)) if t else ""
    titles[title] += 1
    if not title: flag("title-saknas", rel)
    elif len(title) < 15: flag("title-kort", rel, f"{len(title)}: {title}")
    elif len(title) > 62: flag("title-lang", rel, f"{len(title)}: {title}")

    m = re.search(r'<meta name="description" content="(.*?)"', h)
    desc = H.unescape(m.group(1)) if m else ""
    metas[desc] += 1
    if not desc: flag("meta-saknas", rel)
    elif len(desc) < 110: flag("meta-kort", rel, f"{len(desc)}")
    elif len(desc) > 160: flag("meta-lang", rel, f"{len(desc)}")

    c = re.search(r'<link rel="canonical" href="(.*?)"', h)
    if not c: flag("canonical-saknas", rel)
    elif not c.group(1).startswith("https://reliningkoll.se"): flag("canonical-fel", rel, c.group(1))
    else:
        want = BASE + url_of(rel)
        if c.group(1) != want and c.group(1) != want.rstrip("/") + "/":
            flag("canonical-avvikelse", rel, f"{c.group(1)} != {want}")

    if 'name="viewport"' not in h: flag("viewport-saknas", rel)
    if 'lang="sv"' not in h: flag("lang", rel)
    if 'name="robots"' not in h: flag("robots-meta", rel)

    heads = re.findall(r"<h([1-6])[^>]*>", h)
    h1n = heads.count("1")
    if h1n == 0: flag("h1-saknas", rel)
    elif h1n > 1: flag("h1-flera", rel, str(h1n))
    hs = [int(x) for x in heads]
    prev = 0
    for x in hs:
        if prev and x > prev + 1: flag("rubrikhopp", rel, f"h{prev}->h{x}")
        prev = x

    # rubriktext för h1
    hm = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    if hm: h1s[re.sub(r"<[^>]+>", "", hm.group(1)).strip()] += 1

    for prop in ["og:title", "og:description", "og:image", "og:url", "og:type"]:
        if f'property="{prop}"' not in h: flag("og-saknas", rel, prop)
    for nm in ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]:
        if f'name="{nm}"' not in h: flag("twitter-saknas", rel, nm)
    if 'rel="icon"' not in h and 'rel="apple-touch-icon"' not in h: flag("favicon-saknas", rel)

    # JSON-LD
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    for ld in lds:
        try: json.loads(ld)
        except Exception as e: flag("jsonld-ogiltig", rel, str(e)[:60])
    if not lds: flag("jsonld-saknas", rel)

    # bilder
    for tag in re.findall(r"<img[^>]*>", h):
        if "alt=" not in tag: flag("img-alt-saknas", rel, tag[:80])
        src = re.search(r'src="([^"]+)"', tag)
        if src and src.group(1).startswith("/") and not exists(src.group(1)):
            flag("img-trasig", rel, src.group(1))
        if "width=" not in tag or "height=" not in tag: flag("img-dim-saknas", rel, tag[:80])
        if "loading=" not in tag: flag("img-lazy-saknas", rel, tag[:80])

    # interna länkar
    for a in re.findall(r'<a\s([^>]*)>(.*?)</a>', h, re.S):
        attrs, text = a
        href = re.search(r'href="([^"]+)"', attrs)
        if not href: continue
        u = href.group(1)
        if u.startswith("/"):
            links_out[rel].add(url_of(rel))
            links_out[rel].add(u)
            if not exists(u): flag("lank-trasig", rel, u)
            links_in[u.rstrip("/") + "/" if not u.endswith(".html") else u].add(rel)
            txt = re.sub(r"<[^>]+>", "", text).strip()
            if not txt: flag("lank-tom-text", rel, u)
            elif txt.lower() in ("klicka här", "läs mer", "här", "mer"): flag("lank-svag-ankartext", rel, f"{txt} -> {u}")
    if 'href="mailto:' in h or 'href="mailto:' in h: pass

# dubbletter
for t, n in titles.items():
    if n > 1 and t.strip(): flag("title-dubblett", "-", f"{n}x {t[:60]}")
for m, n in metas.items():
    if n > 1 and m.strip(): flag("meta-dubblett", "-", f"{n}x {m[:60]}")
for hh, n in h1s.items():
    if n > 1 and hh: flag("h1-dubblett", "-", f"{n}x {hh[:60]}")

print("=" * 70)
print(f"SIDOR GRANSKADE: {len([r for r in pages if not r.endswith('404.html')])}")
print("=" * 70)
if not issues:
    print("INGA FYND.")
else:
    for k in sorted(issues, key=lambda x: -len(issues[x])):
        v = issues[k]
        print(f"\n[{k}]  {len(v)}")
        for rel, d in v[:6]:
            print(f"    {rel}  {d}")
        if len(v) > 6: print(f"    ... +{len(v)-6} fler")
