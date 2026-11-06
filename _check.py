import os, re, glob
ROOT="/home/clawd/reliningkoll"
pages={}
for f in glob.glob(ROOT+"/**/*.html", recursive=True):
    if "/_preview/" in f: continue
    rel=f.replace(ROOT,"")
    pages[rel]=open(f,encoding="utf-8").read()

def exists(link):
    if link.startswith("/"):
        p=ROOT+link
        if p.endswith("/"): p=p+"index.html"
        if os.path.isfile(p): return True
        if os.path.isfile(p+"/index.html"): return True
        return False
    return True

broken=[]
for rel,html in pages.items():
    for m in re.findall(r'href="(/[^"#?]*)"', html):
        if not exists(m):
            broken.append((rel,m))
print("Sidor:", len(pages))
print("Trasiga interna lankar:", len(broken))
for b in broken[:40]: print("  ", b)

titles={}
for rel,html in pages.items():
    t=re.search(r"<title>(.*?)</title>", html)
    if t: titles.setdefault(t.group(1),[]).append(rel)
dups={k:v for k,v in titles.items() if len(v)>1 and k.strip()}
print("\nDubblett-titlar:", len(dups))
for k,v in list(dups.items())[:10]: print("  ", k, "->", v[:4])

metas={}
for rel,html in pages.items():
    m=re.search(r'<meta name="description" content="(.*?)"', html)
    if m: metas.setdefault(m.group(1),[]).append(rel)
dupmeta={k:v for k,v in metas.items() if len(v)>1 and k.strip()}
print("\nDubblett-meta:", len(dupmeta))
for k,v in list(dupmeta.items())[:10]: print("  ", k[:70], "->", v[:4])
