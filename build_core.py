#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger hela reliningkoll.se som statisk sajt."""
import os, json, re, html as H, datetime

ROOT = "/home/clawd/reliningkoll"
BASE = "https://reliningkoll.se"
TODAY = "2026-11-06"
FORM_EMAIL = "hej@reliningkoll.se"   # aktiveras hos formsubmit.co

def esc(s): return H.escape(str(s), quote=True)

# ---------------------------------------------------------------- shell
NAV = [("/pris/", "Priser"), ("/guider/", "Guider"), ("/relining/", "Hitta firmor"),
       ("/for-proffs/", "För proffs")]

def head(title, desc, path, schema="", og="og.png", noindex=False):
    title = re.sub(r"\s*\|\s*Reliningkoll\s*$", "", title).strip()
    canonical = BASE + path
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta name="theme-color" content="#08312f">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Reliningkoll">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="sv_SE">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/{og}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/archivo-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css">
{schema}
</head>
<body>
<a class="skip-link" href="#main">Hoppa till innehåll</a>
<header class="site">
  <div class="wrap">
    <nav class="nav" aria-label="Huvudmeny">
      {logo_link()}
      <ul>
        {''.join(f'<li><a href="{u}">{t}</a></li>' for u, t in NAV)}
      </ul>
      <a class="nav-cta" href="/offert/">Få 3 offerter</a>
      <button class="menu-btn" aria-label="Meny" aria-expanded="false"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>
<main id="main">
'''

def logo_link():
    return ('<a class="logo" href="/" aria-label="Reliningkoll startsida">'
            '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<path d="M12 2.5c3.6 4.1 6 7.5 6 10.6A6 6 0 0 1 6 13.1c0-3.1 2.4-6.5 6-10.6Z" fill="#0f6f67"/>'
            '<path d="M9 13.4a3 3 0 0 0 3 3" stroke="#eaf5f3" stroke-width="1.6" stroke-linecap="round"/></svg>'
            'Relining<b>koll</b></a>')

FOOT = f'''</main>
<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        {logo_link()}
        <p class="small" style="max-width:280px">Oberoende jämförelsetjänst för relining, avloppsspolning och rörinspektion. Kostnadsfritt för dig som privatperson.</p>
      </div>
      <div><p class="foot-h">Jämför</p><ul>
        <li><a href="/pris/">Priser &amp; kostnader</a></li>
        <li><a href="/guider/">Guider</a></li>
        <li><a href="/relining/">Relining i din kommun</a></li>
        <li><a href="/avloppsspolning/">Avloppsspolning</a></li>
        <li><a href="/rorinspektion/">Rörinspektion</a></li>
        <li><a href="/offert/">Få offerter gratis</a></li>
      </ul></div>
      <div><p class="foot-h">För proffs</p><ul>
        <li><a href="/for-proffs/">Anslut ditt företag</a></li>
        <li><a href="/foretag/">Så granskar vi firmor</a></li>
      </ul></div>
      <div><p class="foot-h">Om tjänsten</p><ul>
        <li><a href="/om-oss/">Om oss</a></li>
        <li><a href="/integritetspolicy/">Integritetspolicy</a></li>
        <li><a href="/anvandarvillkor/">Användarvillkor</a></li>
        <li><a href="mailto:{FORM_EMAIL}">Kontakt</a></li>
      </ul></div>
    </div>
    <div class="foot-bottom">
      <span>&copy; 2026 Reliningkoll &middot; Oberoende jämförelse av relining</span>
      <span>Vi förmedlar kontakt med granskade entreprenörer. Ingen bindningstid.</span>
    </div>
  </div>
</footer>
<script src="/assets/app.js" defer></script>
</body>
</html>'''

_STYLEMAP = {
 "max-width:280px": "s-280w", "padding-top:0": "s-pt0", "margin-top:40px": "s-mt40",
 "margin-bottom:24px": "s-mb24", "width:100%": "s-w100", "font-size:22px": "s-h2sm",
 "color:#5c6b69": "s-kalla", "max-width:640px;margin:0 auto": "s-c640",
 "margin-top:16px": "s-mt16", "color:var(--muted)": "s-muted", "align-items:start": "s-start",
 "justify-content:center": "s-center",
}

def _strip_inline(html):
    if "<" not in html: return html
    def repl(m):
        tag = m.group(0)
        sm = re.search(r'style="([^"]*)"', tag)
        if not sm: return tag
        cls = _STYLEMAP.get(sm.group(1).strip())
        if not cls: return tag
        tag2 = re.sub(r'\s*style="[^"]*"', "", tag)
        if 'class="' in tag2:
            tag2 = tag2.replace('class="', f'class="{cls} ', 1)
        else:
            tag2 = tag2[:-1] + f' class="{cls}">'
        return tag2
    return re.sub(r'<[a-zA-Z][^>]*style="[^"]*"[^>]*>', repl, html)

def write(path, html):
    p = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(_strip_inline(html))
    print("  ", path)

FAQ_DEFAULT = [
 ("Vad kostar relining?", "För en villa ligger komplett relining oftast mellan 80 000 och 250 000 kr före ROT-avdrag. Per meter rör räknar man vanligen 800 till 1 500 kr. Exakt pris beror på rörlängd, material och åtkomst."),
 ("Är offerterna verkligen gratis?", "Ja. Tjänsten är kostnadsfri för dig som privatperson och du har ingen skyldighet att anlita någon av firmorna. Företagen betalar en avgift per förfrågan de väljer att ta del av."),
 ("Hur många företag kontaktar mig?", "Vi matchar dig med upp till tre lokala entreprenörer som arbetar i din kommun. Du jämför deras offerter och väljer själv om du vill gå vidare."),
 ("Kan jag använda ROT-avdraget på relining?", "Ja. Arbetskostnaden för relining i egen villa är ROT-berättigad. Avdraget är 30 procent av arbetskostnaden, med ett tak på 50 000 kr per person och år."),
 ("Hur länge håller relining?", "En korrekt utförd relining håller normalt 40 till 50 år. Livslängden beror på metod, rörmaterial och att installationen görs enligt branschregler."),
 ("Vem betalar vid relining i en bostadsrättsförening?", "Vid relining av stammarna betalar föreningen normalt hela arbetet ur sitt underhållsansvar. Du som äger lägenheten svarar för återställande av ytskikt i ditt eget badrum."),
]

def f(msg):  # formaterar callout
    return f'<div class="callout"><p>{msg}</p></div>'

def logo_ph(name):
    return ''.join(w[0] for w in name.split()[:2]).upper()


# ================================================================ HEM
def build_home():
    schema = json.dumps({
      "@context":"https://schema.org","@graph":[
        {"@type":"WebSite","@id":BASE+"/#website","url":BASE+"/","name":"Reliningkoll",
         "inLanguage":"sv-SE","publisher":{"@id":BASE+"/#org"}},
        {"@type":"Organization","@id":BASE+"/#org","name":"Reliningkoll","url":BASE+"/",
         "description":"Oberoende jämförelsetjänst för relining, avloppsspolning och rörinspektion i hela Sverige.",
         "areaServed":{"@type":"Country","name":"Sverige"},"email":FORM_EMAIL},
        {"@type":"Service","name":"Jämför relining-offerter","serviceType":"Offertförmedling relining",
         "provider":{"@id":BASE+"/#org"},"areaServed":{"@type":"Country","name":"Sverige"}}
      ]}, ensure_ascii=False)
    faq = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ_DEFAULT]},
        ensure_ascii=False)
    html = head("Relining – pris, metoder och offerter från lokala firmor | Reliningkoll",
        "Jämför relining och avloppsrenovering gratis. Få upp till 3 offerter från granskade reliningfirmor i din kommun. Prisguider, metoder och svar på vanliga frågor.",
        "/", f'<script type="application/ld+json">{schema}</script>\n<script type="application/ld+json">{faq}</script>')
    html += f'''
<section class="hero"><div class="wrap"><div class="hero-grid">
  <div>
    <h1 class="h1">Få upp till tre offerter på <b>relining</b> från lokala firmor</h1>
    <p class="lead">Gratis, utan förpliktelse. Vi matchar din villa, bostadsrätt eller fastighet med kvalitetsgranskade entreprenörer i din kommun så att du kan jämföra pris och metod på riktigt.</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="/offert/">Få 3 offerter gratis</a>
      <a class="btn btn-ghost btn-lg" href="/pris/">Se priser först</a>
    </div>
    <div class="trust">
      <span><svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Granskade entreprenörer</span>
      <span><svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Kostnadsfritt</span>
      <span><svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Ingen bindningstid</span>
    </div>
    <div class="hero-stamp"><span class="stamp">Gratis för dig &middot; ingen bindningstid</span></div>
  </div>
  <div class="quote-card">
    <h2>Berätta om ditt projekt</h2>
    <p class="small">Tar under en minut. Du får svar från firmor i ditt område.</p>
    <form data-lead action="https://formsubmit.co/{FORM_EMAIL}" method="POST">
      <input type="hidden" name="_subject" value="Ny reliningförfrågan">
      <input type="hidden" name="_captcha" value="false">
      <div class="field"><label for="cf-typ">Vad gäller det?</label>
        <select id="cf-typ" name="typ" required>
          <option value="">Välj</option><option>Relining av avloppsrör</option>
          <option>Relining villa</option><option>Relining bostadsrätt/BRF</option>
          <option>Relining av gjutjärnsrör</option><option>Avloppsspolning</option>
          <option>Rörinspektion</option><option>Vet inte, behöver rådgivning</option>
        </select></div>
      <div class="field"><label for="cf-post">Postnummer</label>
        <input id="cf-post" name="postnummer" inputmode="numeric" placeholder="t.ex. 652 24" required></div>
      <div class="field"><label for="cf-tel">Telefon</label>
        <input id="cf-tel" name="telefon" type="tel" placeholder="07x xxx xx xx" required></div>
      <div class="field"><label for="cf-mail">E-post</label>
        <input id="cf-mail" name="epost" type="email" placeholder="namn@exempel.se" required></div>
      <button class="btn btn-dark btn-lg" type="submit" style="width:100%">Få mina offerter</button>
      <p class="form-note">Gratis och utan förpliktelse. Vi delar aldrig dina uppgifter med fler än 3 firmor.</p>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</div></div></section>

<section class="bg-card"><div class="wrap">
  <div class="sec-head rv">
    <h2>Från förfrågan till färdig offert</h2>
    <p>Du behöver bara beskriva ditt projekt en gång. Resten sköter vi.</p></div>
  <div class="steps">
    <div class="step rv"><div class="num">1</div><h3>Beskriv projektet</h3>
      <p>Fyll i vad det gäller, var i landet och ungefär hur stort. Det tar under en minut.</p></div>
    <div class="step rv"><div class="num">2</div><h3>Vi matchar dig</h3>
      <p>Din förfrågan granskas manuellt och skickas till upp till tre lokala entreprenörer i din kommun.</p></div>
    <div class="step rv"><div class="num">3</div><h3>Jämför och välj</h3>
      <p>Du får offerter att jämföra i lugn och ro. Du bestämmer helt själv om och med vem du går vidare.</p></div>
  </div>
</div></section>

<section><div class="wrap"><p class="reveal-tag">Relining förnyar rören inifrån &mdash; utan att du behöver riva golv, väggar eller trädgård.</p></div></section>

<section><div class="wrap">
  <div class="sec-head rv">
    <h2>Det här hjälper vi dig med</h2>
    <p>Allt inom invändig rörrenovering. Välj det som passar ditt ärende.</p></div>
  <div class="grid grid-3">
    <a class="card rv" href="/pris/relining/"><div class="num">R</div><h3>Relining</h3>
      <p>Förnya avloppsrör invändigt med strumpa eller UV-härdning. Slipp stambyte och rivning.</p></a>
    <a class="card rv" href="/avloppsspolning/"><div class="num">S</div><h3>Avloppsspolning</h3>
      <p>Stopp i avloppet? Få hjälp av en spolfirma med rätt utrustning och kamera.</p></a>
    <a class="card rv" href="/rorinspektion/"><div class="num">I</div><h3>Rörinspektion</h3>
      <p>Kamerainspektion visar rörens skick innan du bestämmer åtgärd.</p></a>
    <a class="card rv" href="/guider/relining-av-gjutarror/"><div class="num">G</div><h3>Gjutjärnsrör</h3>
      <p>Så renoverar man gamla gjutjärns- och betongrör utan att gräva.</p></a>
    <a class="card rv" href="/pris/relining-brf/"><div class="num">B</div><h3>BRF &amp; fastighet</h3>
      <p>Relining av stammar i bostadsrättsföreningar och flerfamiljshus.</p></a>
    <a class="card rv" href="/guider/relining-av-skorsten/"><div class="num">K</div><h3>Skorsten</h3>
      <p>Infodring av rökkanaler och ventilationskanaler med rätt godkännande.</p></a>
  </div>
</div></section>

<section class="bg-card"><div class="wrap">
  <div class="sec-head rv"><h2>Vad kostar relining?</h2>
    <p>Riktpriser för 2026. Räkna alltid hem en individuell offert, men det här ger dig ett hum.</p></div>
  <div class="grid grid-2" style="align-items:start">
    <table class="tbl rv"><thead><tr><th>Objekt</th><th>Riktpris</th></tr></thead><tbody>
      <tr><td>Villa, komplett system</td><td>80 000 – 250 000 kr</td></tr>
      <tr><td>Lägenhet, per stam</td><td>50 000 – 120 000 kr</td></tr>
      <tr><td>Per meter rör</td><td>800 – 1 500 kr</td></tr>
      <tr><td>Rörinspektion med kamera</td><td>0 – 2 500 kr</td></tr>
      <tr><td>Avloppsspolning</td><td>1 500 – 4 500 kr</td></tr>
    </tbody></table>
    <div class="rv">{f("Priserna är riktpriser före ROT-avdrag. Villaarbeten är ROT-berättigade, vilket ger 30 % av arbetskostnaden tillbaka, upp till 50 000 kr per person och år.")}
      <p class="body" style="color:var(--muted)">Vill du se hur priset byggs upp? Läs hela prisguiden med kostnad per meter, villa och bostadsrätt.</p>
      <p style="margin-top:16px"><a class="btn btn-dark" href="/pris/">Öppna prisguiden</a></p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head rv"><h2>Lär dig innan du beställer</h2>
    <p>Metoder, kostnader och fallgropar, förklarat utan krångel.</p></div>
  <div class="grid grid-3">
    <a class="card rv" href="/guider/vad-ar-relining/"><h3>Vad är relining?</h3><p>Metoden, hur den går till och när den passar.</p></a>
    <a class="card rv" href="/guider/relining-eller-stambyte/"><h3>Relining eller stambyte?</h3><p>Kostnad, tid och livslängd jämfört rakt upp och ner.</p></a>
    <a class="card rv" href="/guider/nackdelar-med-relining/"><h3>Nackdelar med relining</h3><p>När relining inte är rätt val. Ärligt och konkret.</p></a>
    <a class="card rv" href="/guider/hur-lange-haller-relining/"><h3>Hur länge håller relining?</h3><p>Livslängd, garanti och vad som påverkar hållbarheten.</p></a>
    <a class="card rv" href="/guider/strumpmetoden/"><h3>Strumpmetoden</h3><p>Så fungerar den vanligaste reliningmetoden steg för steg.</p></a>
    <a class="card rv" href="/guider/"><h3>Alla guider</h3><p>Se hela kunskapsbiblioteket om relining och avlopp.</p></a>
  </div>
</div></section>

<section class="bg-card"><div class="wrap">
  <div class="sec-head rv"><h2>Relining i din kommun</h2>
    <p>Vi förmedlar firmor i hela landet. Välj din kommun för lokala priser och entreprenörer.</p></div>
  <div class="pills rv" id="city-pills"></div>
</div></section>

<section><div class="wrap narrow">
  <div class="sec-head rv"><h2>Vanliga frågor</h2></div>
  <div class="faq rv">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in FAQ_DEFAULT)}</div>
</div></section>

<section><div class="wrap"><div class="cta-band rv">
  <h2>Redo att jämföra relining?</h2>
  <p>Beskriv ditt projekt och få upp till tre offerter från lokala firmor. Gratis och utan förpliktelse.</p>
  <a class="btn btn-primary btn-lg" href="/offert/">Få offerter nu</a>
</div></div></section>
'''
    html += FOOT
    # fyll kommun-piller med JS-lista
    write("/index.html", html)


# ================================================================ sidmall
def page(title, desc, path, body, schema="", crumb=None, faq=None, noindex=False):
    s = ""
    if schema: s += f'<script type="application/ld+json">{schema}</script>\n'
    if faq:
        s += '<script type="application/ld+json">' + json.dumps(
            {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
            ensure_ascii=False) + '</script>\n'
    if crumb:
        s += '<script type="application/ld+json">' + json.dumps(
            {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
                {"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(crumb)]},
            ensure_ascii=False) + '</script>\n'
    h = head(title, desc, path, s, noindex=noindex)
    h += body + FOOT
    return h

def crumb_html(items):
    parts = []
    for i,(n,u) in enumerate(items):
        if i == len(items)-1: parts.append(f'<span>{esc(n)}</span>')
        else: parts.append(f'<a href="{u}">{esc(n)}</a>')
    return '<div class="crumb">' + ' / '.join(parts) + '</div>'
