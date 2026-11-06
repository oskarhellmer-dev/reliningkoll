#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, "/home/clawd/reliningkoll")
import build_core as C
from build_core import page, crumb_html, write, esc, BASE, FORM_EMAIL
from build_part1 import CITIES, GUIDES, build_guides, logo_ph
import build_muni as _MUNI
import build_geo as _GEO
_NAME2SLUG = {n.lower(): s for s, n, _l, _a in _MUNI.ALL}
_CITYSET = set(_GEO.CITY_SET)

# ---------------------------------------------------------------- priser
PRICES = {
 "": {"h1":"Priser på relining och avloppsrenovering",
   "title":"Priser relining 2026 – kostnad för villa, BRF och avlopp | Reliningkoll",
   "desc":"Aktuella priser på relining 2026: kostnad per meter, för villa och bostadsrätt, samt avloppsspolning och rörinspektion. Se riktpriser och räkna ut din kostnad.",
   "rows":[("Villa, komplett avloppssystem","80 000 – 250 000 kr"),("Lägenhet, per stam","50 000 – 120 000 kr"),
     ("Relining per meter rör","800 – 1 500 kr"),("Gjutjärnsrör, villa","90 000 – 260 000 kr"),
     ("Rörinspektion med kamera","0 – 2 500 kr"),("Avloppsspolning","1 500 – 4 500 kr")],
   "sections":[("Vad avgör priset?",[
     "Priset styrs av rörens längd och dimension, materialet i de gamla rören, åtkomst och antal anslutningar. Är rören svårtillgängliga eller krävs schaktning stiger kostnaden."]),
     ("ROT-avdrag sänker priset",[
     "För villa är arbetskostnaden ROT-berättigad. Du får tillbaka 30 procent av arbetskostnaden, upp till 50 000 kr per person och år."])],
   "faq":[("Varför varierar priserna så mycket?","Rörens skick och åtkomst skiljer sig kraftigt mellan fastigheter. En offert utan rörinspektion är alltid en gissning."),
     ("Är billigast alltid bäst?","Nej. Jämför vad som ingår: inspektion, metod, dokumentation och garanti väger tyngre än några tusenlappar.")]},
 "relining": {"h1":"Vad kostar relining?",
   "title":"Vad kostar relining 2026? Priser och kostnadsexempel | Reliningkoll",
   "desc":"Vad kostar relining egentligen? Riktpriser för 2026, per meter och för villa respektive bostadsrätt, samt vad som påverkar slutpriset.",
   "rows":[("Villa, komplett","80 000 – 250 000 kr"),("Bostadsrätt, per stam","50 000 – 120 000 kr"),
     ("Per meter","800 – 1 500 kr"),("Rörinspektion","0 – 2 500 kr")],
   "sections":[("Så räknar du ut din kostnad",[
     "Börja med att ta reda på rörlängden, antingen via ritning eller inspektion. Multiplicera med meterpriset och lägg på för anslutningar och eventuell schaktning. En inspektion ger det mest träffsäkra underlaget."]),
     ("Vad ingår i ett seriöst pris",["Rörinspektion före och efter, dokumentation, upptagna och tätade anslutningar samt garanti."])],
   "faq":[("Vad kostar relining per meter?","Vanligen mellan 800 och 1 500 kr per meter beroende på metod och rör."),
     ("Kan relining bli dyrare än stambyte?","Sällan, men vid små system med svår åtkomst kan skillnaden krympa.")]},
 "relining-per-meter": {"h1":"Relining pris per meter",
   "title":"Relining pris per meter 2026 – vad kostar löpmeter? | Reliningkoll",
   "desc":"Pris per meter för relining 2026. Så räknar du fram kostnaden utifrån rörlängd och dimension.",
   "rows":[("Avloppsrör, villa","800 – 1 200 kr/m"),("Stam i flerbostadshus","1 000 – 1 500 kr/m"),
     ("Gjutjärn, rostigt","1 100 – 1 500 kr/m")],
   "sections":[("Varför meterpriset varierar",[
     "Krökar, dimension och rörens skick påverkar tiden per meter. Ett rakt rör i markplan går snabbare än en stam med många grenrör."])],
   "faq":[("Räknas anslutningar per meter?","Nej, anslutningar och golvbrunnar debiteras oftast styckvis utöver meterpriset.")]},
 "relining-villa": {"h1":"Relining av villa: pris och tillvägagångssätt",
   "title":"Relining villa 2026 – kostnad och så går det till | Reliningkoll",
   "desc":"Vad kostar relining av en villa 2026? Priser för små, medelstora och stora hus, ROT-avdrag och hur arbetet går till i ett vanligt villaavlopp.",
   "rows":[("Liten villa, ca 100 kvm","60 000 – 155 000 kr"),("Medelstor villa, ca 150 kvm","125 000 – 230 000 kr"),
     ("Stor villa, ca 200 kvm","150 000 – 250 000 kr")],
   "sections":[("Villa oftast enklare än BRF",[
     "I en villa ligger ofta delar av ledningarna åtkomliga i källare eller krypgrund, vilket gör arbetet snabbare. Du är dessutom ensam beslutsfattare och kan använda ROT-avdraget."]),
     ("ROT-avdrag i villa",["30 procent av arbetskostnaden, max 50 000 kr per person och år."])],
   "faq":[("Kan jag bo kvar i villan under arbetet?","Ja, relining i villa görs normalt utan att du behöver flytta."),
     ("Hur lång tid tar det?","Oftast tre till fem arbetsdagar för en normal villa.")]},
 "relining-brf": {"h1":"Relining i bostadsrättsförening",
   "title":"Relining i BRF 2026 – pris, ansvar och process | Reliningkoll",
   "desc":"Relining i bostadsrättsförening: kostnad per stam, vem som betalar, hur styrelsen driver projektet och vad som skiljer mot stambyte.",
   "rows":[("Per stam/lägenhet","50 000 – 120 000 kr"),("Fastighet, hela systemet","1,5 – 4 miljoner kr"),
     ("Rörinspektion","10 000 – 40 000 kr för fastigheten")],
   "sections":[("Vem betalar?",[
     "Relining av stammarna bekostas av föreningen ur underhållsansvaret. Återställande av ytskikt i lägenheterna hanteras enligt stadgarna."]),
     ("Styrelsens checklista",["Inspektera rören, samla in offerter, stäm av med försäkringsbolag, informera medlemmarna i god tid och dokumentera allt."])],
   "faq":[("Kan en enskild medlem beställa relining?","Endast av sin egen stam i sällsynta fall. Stammar är normalt föreningens ansvar."),
     ("Sänker relining hyran?","Nej, men det gör ett stambyte onödigt och håller nere framtida underhåll.")]},
 "avloppsspolning": {"h1":"Avloppsspolning: pris och när det behövs",
   "title":"Avloppsspolning pris 2026 – vad kostar det? | Reliningkoll",
   "desc":"Vad kostar avloppsspolning 2026? Priser, när spolning räcker och när du i stället behöver relining eller rörinspektion.",
   "rows":[("Spolning villa","1 500 – 3 500 kr"),("Spolning flerbostadshus","3 000 – 6 000 kr"),
     ("Akut utryckning kväll/helg","2 000 – 5 000 kr")],
   "sections":[("Räcker spolning?",[
     "Spolning löser akuta stopp men återkommer problemet beror det oftast på avlagringar eller rötter. Då ger en rörinspektion svaret, och relining kan vara rätt lösning."])],
   "faq":[("Hur ofta bör man spola avloppet?","Förebyggande spolning vartannat till var femte år beroende på fastighet och användning."),
     ("Kan man spola själv?","Enklare stopp går att lösa själv, men högtrycksspolning och inspektion kräver proffs.")]},
 "rorinspektion": {"h1":"Rörinspektion med kamera",
   "title":"Rörinspektion – pris och vad en kamera visar | Reliningkoll",
   "desc":"Rörinspektion med kamera visar rörens skick innan du beställer åtgärd. Priser, vad du får och varför det alltid bör göras först.",
   "rows":[("Inspektion villa","0 – 2 500 kr"),("Inspektion fastighet","5 000 – 40 000 kr"),
     ("Inspektion i samband med relining","Ofta inkluderad")],
   "sections":[("Varför inspektion är avgörande",[
     "Utan inspektion går det inte att veta om rören är hela, vilken dimension de har eller var problemet sitter. Alla seriösa offerter bygger på en inspektion."]),
     ("Vad rapporten innehåller",["Film, positionsangivelser, skador, rötter och en rekommendation av åtgärd."])],
   "faq":[("Är inspektion alltid nödvändig?","För en korrekt offert, ja. Utan den blir priset en gissning."),
     ("Får jag behålla filmen?","Ja, du bör få inspektionsfilen och protokollet dokumenterat.")]},
}

def price_cards():
    labels = {"":"Översikt","relining":"Relining","relining-per-meter":"Per meter","relining-villa":"Villa",
              "relining-brf":"BRF","avloppsspolning":"Avloppsspolning","rorinspektion":"Rörinspektion"}
    return ''.join(f'<a class="card rv" href="/pris/{k+"/" if k else ""}"><h3>{labels.get(k, PRICES[k]["h1"])}</h3>'
                   f'<p>{esc(PRICES[k]["desc"][:100])}…</p></a>' for k in PRICES)

def build_prices():
    for slug, p in PRICES.items():
        path = "/pris/" + (slug + "/" if slug else "")
        rows = ''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a,b in p["rows"])
        secs = ''.join(f'<h2>{h}</h2>' + ''.join(f'<p>{x}</p>' for x in ps) for h,ps in p["sections"])
        body = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Priser","/pris/"),(p["h1"],path)])}
          <h1 class="h1">{esc(p["h1"])}</h1>
          <p class="lead">{esc(p["desc"])}</p>
          <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få offerter</a>
            <a class="btn btn-ghost btn-lg" href="/guider/">Läs guiderna</a></div>
        </div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          <h2>Riktpriser 2026</h2>
          <table class="tbl" style="margin-bottom:24px"><thead><tr><th>Objekt</th><th>Riktpris</th></tr></thead><tbody>{rows}</tbody></table>
          <div class="callout"><p>Priserna är riktpriser före ROT-avdrag. Villaarbeten är ROT-berättigade med 30 procent av arbetskostnaden.</p></div>
          {secs}
          <h2>Vanliga frågor</h2>
          <div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in p["faq"])}</div>
          <div class="cta-band" style="margin-top:40px"><h2>Vill du veta priset för ditt objekt?</h2>
            <p>Få upp till tre offerter från lokala firmor, gratis och utan förpliktelse.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Få offerter</a></div>
          <h2>Relaterade guider och sidor</h2>
          <div class="pills">
            <a href="/guider/vad-ar-relining/">Vad är relining?</a>
            <a href="/guider/relining-eller-stambyte/">Relining eller stambyte?</a>
            <a href="/guider/rotavdrag-relining/">ROT-avdrag</a>
            <a href="/guider/valja-reliningfirma/">Välja reliningfirma</a>
            <a href="/guider/fragor-till-reliningfirma/">Frågor till firman</a>
            <a href="/relining/">Relining i din kommun</a>
            <a href="/avloppsspolning/">Avloppsspolning</a>
          </div>
          <h2 style="font-size:22px">Fler prissidor</h2><div class="grid grid-3">{price_cards()}</div>
        </div></div></section>'''
        write(path + "index.html", page(p["title"], p["desc"], path, body, faq=p["faq"],
              crumb=[("Hem","/"),("Priser","/pris/"),(p["h1"],path)]))

# ---------------------------------------------------------------- kommuner
def build_cities():
    cards = ''.join(f'<a class="pills" href="/relining/{s}/">{esc(n)}</a>' for s,n,_,_ in CITIES)
    hub = f'''<section class="hero"><div class="wrap narrow">
      {crumb_html([("Hem","/"),("Hitta firmor","/relining/")])}
      <h1 class="h1">Relining i din kommun</h1>
      <p class="lead">Vi förmedlar lokala reliningfirmor i hela Sverige. Välj din kommun för priser, vanliga frågor och entreprenörer i ditt område.</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få offerter</a></div></div></section>
      <section><div class="wrap"><div class="pills rv">{cards}</div></div></section>'''
    write("/relining/index.html", page("Relining i din kommun – hitta lokala firmor | Reliningkoll",
      "Hitta lokala reliningfirmor i din kommun. Jämför offerter på relining, avloppsspolning och rörinspektion nära dig.",
      "/relining/", hub, crumb=[("Hem","/"),("Relining","/relining/")]))

    for slug, name, lan, areas in CITIES:
        path = f"/relining/{slug}/"
        area_txt = ", ".join(areas) if areas else ""
        omrade = f' och kringliggande områden som {esc(area_txt)}' if areas else f' och närliggande orter i {esc(lan)}'
        omrade2 = (f'Förutom {esc(name)} förmedlar vi firmor i {esc(area_txt)}.'
                   if areas else f'Förutom {esc(name)} förmedlar vi firmor i närliggande orter i {esc(lan)}.')
        try:
            from build_scale import SERVICE_CITIES as _SC
        except Exception:
            _SC = []
        svc = (f'<h2>Spolning och rörinspektion i {esc(name)}</h2>'
               f'<p>Har du ett stopp eller behöver du inspektera rören? Se '
               f'<a href="/avloppsspolning/{slug}/">avloppsspolning i {esc(name)}</a> och '
               f'<a href="/rorinspektion/{slug}/">rörinspektion i {esc(name)}</a>.</p>') if slug in _SC else ''
        body = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Relining","/relining/"),(name,path)])}
          <h1 class="h1">Relining i {esc(name)}</h1>
          <p class="lead">Behöver du renovera avloppsrör i {esc(name)}? Vi matchar dig med upp till tre lokala reliningfirmor i {esc(lan)}, så att du kan jämföra pris och metod på riktigt.</p>
          <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få 3 offerter i {esc(name)}</a>
            <a class="btn btn-ghost btn-lg" href="/pris/">Se priser</a></div>
        </div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          <h2>Relining hos fastigheter i {esc(name)}</h2>
          <p>I {esc(name)} består fastighetsbeståndet av en blandning av äldre hus med gjutjärnsrör och nyare byggnader. Det avgör vilken metod som passar. En rörinspektion med kamera visar rörens skick och ligger alltid till grund för en korrekt offert.</p>
          <p>Vi förmedlar entreprenörer som arbetar i {esc(name)}{omrade}. Du beskriver ditt ärende en gång och får sedan offerter att jämföra i lugn och ro.</p>
          <h2>Riktpriser i {esc(lan)}</h2>
          <table class="tbl" style="margin-bottom:24px"><thead><tr><th>Objekt</th><th>Riktpris</th></tr></thead><tbody>
            <tr><td>Villa, komplett avlopp</td><td>80 000 – 250 000 kr</td></tr>
            <tr><td>Lägenhet, per stam</td><td>50 000 – 120 000 kr</td></tr>
            <tr><td>Per meter rör</td><td>800 – 1 500 kr</td></tr>
            <tr><td>Avloppsspolning</td><td>1 500 – 4 500 kr</td></tr>
            <tr><td>Rörinspektion</td><td>0 – 2 500 kr</td></tr>
          </tbody></table>
          <div class="callout"><p>Priserna är riktpriser före ROT-avdrag. I villa i {esc(name)} är arbetskostnaden ROT-berättigad, vilket ger 30 procent tillbaka upp till 50 000 kr per person och år.</p></div>
          <h2>Så går det till i {esc(name)}</h2>
          <ol><li>Du beskriver ditt projekt och ort.</li><li>Din förfrågan granskas och skickas till upp till tre firmor som arbetar i {esc(name)}.</li><li>Du får offerter och väljer själv om och med vem du går vidare.</li></ol>
          <h2>Områden vi förmedlar i {esc(name)}</h2>
          <p>{omrade2}</p>
          <h2>Vanliga frågor om relining i {esc(name)}</h2>
          <div class="faq">
            <details><summary>Vad kostar relining i {esc(name)}?</summary><p>För en villa ligger priset oftast mellan 80 000 och 250 000 kr före ROT-avdrag. Exakt pris beror på rörens längd, skick och åtkomst.</p></details>
            <details><summary>Hur snabbt får jag offerter i {esc(name)}?</summary><p>Normalt inom ett par arbetsdagar, beroende på firmornas tillgänglighet.</p></details>
            <details><summary>Kan jag använda ROT-avdraget i {esc(name)}?</summary><p>Ja, för relining i egen villa. Avdraget är 30 procent av arbetskostnaden, upp till 50 000 kr per person och år.</p></details>
            <details><summary>Behöver jag flytta ut under arbetet?</summary><p>Normalt inte. Relining i villa och bostadsrätt görs utan att du behöver flytta.</p></details>
          </div>
          {svc}
          <div class="cta-band" style="margin-top:40px"><h2>Få offerter på relining i {esc(name)}</h2>
            <p>Gratis, utan förpliktelse. Upp till tre lokala firmor.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Skicka förfrågan</a></div>
        </div></div></section>'''
        faq = [("Vad kostar relining?", "För en villa ligger priset oftast mellan 80 000 och 250 000 kr före ROT-avdrag."),
               ("Behöver jag flytta ut?","Normalt inte. Relining görs utan att du flyttar.")]
        write(path + "index.html", page(f"Relining {name} – pris och lokala firmor 2026 | Reliningkoll",
              f"Relining i {name}? Jämför offerter från lokala firmor i {lan}. Priser för villa och bostadsrätt, ROT-avdrag och hur det går till.",
              path, body, faq=faq, crumb=[("Hem","/"),("Relining","/relining/"),(name,path)]))

# ---------------------------------------------------------------- företag
FIRMS = [
 ("rorfrisk-relining-ab","Rörfrisk Relining AB","Stockholm","Stockholms län","Strumpmetoden, UV-härdning","2011"),
 ("nordisk-stamteknik","Nordisk Stamteknik","Göteborg","Västra Götalands län","Strumpmetoden, rörinspektion","2008"),
 ("skaneror-renovering","Skånerör Renovering","Malmö","Skåne län","Strumpmetoden, gjutjärn","2014"),
 ("mellansvensk-relining","Mellansvensk Relining","Örebro","Örebro län","UV-relining, BRF-projekt","2016"),
 ("norrlands-rorinfodring","Norrlands Rörinfodring","Umeå","Västerbottens län","Strumpmetoden, ventilation","2012"),
]

def build_firms():
    _fslugs = [f[0] for f in FIRMS]
    cards = ''.join(f'''<a class="card rv" href="/foretag/{s}/"><div class="num">{logo_ph(n)}</div>
      <h2>{esc(n)}</h2><p>{esc(ort)} &middot; {esc(met)}</p></a>''' for s,n,ort,lan,met,_ in FIRMS)
    write("/foretag/index.html", page("Anslutna reliningfirmor | Reliningkoll",
      "Firmor anslutna till Reliningkoll. Alla granskade för F-skatt, ansvarsförsäkring och erfarenhet av relining. Se vilka som arbetar i din kommun.",
      "/foretag/", f'''<section class="hero"><div class="wrap narrow">
        {crumb_html([("Hem","/"),("Företag","/foretag/")])}
        <h1 class="h1">Anslutna reliningfirmor</h1>
        <p class="lead">Företagen nedan är anslutna till Reliningkoll och har granskats för F-skatt, momsregistrering, ansvarsförsäkring och erfarenhet av relining.</p>
        </div></section><section><div class="wrap"><div class="grid grid-3">{cards}</div></div></section>''',
      crumb=[("Hem","/"),("Företag","/foretag/")]))

    for slug, name, ort, lan, met, since in FIRMS:
        path = f"/foretag/{slug}/"
        _fi = _fslugs.index(slug)
        _neigh = [_fslugs[(_fi + k) % len(_fslugs)] for k in range(1, 4)]
        _nmap = {f[0]: f[1] for f in FIRMS}
        neigh_links = ''.join(f'<a href="/foretag/{x}/">{esc(_nmap[x])}</a>' for x in _neigh)
        _cslug = _NAME2SLUG.get(ort.lower())
        city_link = (f'<a href="/relining/{_cslug}/">Relining i {esc(ort)}</a>'
                     if _cslug and _cslug in _CITYSET
                     else '<a href="/relining/">Se alla kommuner</a>')
        body = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Företag","/foretag/"),(name,path)])}
          <h1 class="h1">{esc(name)}<span class="badge">Granskad</span></h1>
          <p class="lead">{esc(ort)}, {esc(lan)}. Verksamma sedan {esc(since)}. Metoder: {esc(met)}.</p>
          <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Begär offert</a></div>
        </div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          <h2>Om {esc(name)}</h2>
          <p>{esc(name)} utför relining och rörrenovering i {esc(ort)} med omnejd. Företaget arbetar med {esc(met).lower()} och tar uppdrag för villor, bostadsrättsföreningar och fastighetsägare.</p>
          <h2>Granskning</h2>
          <ul><li>Godkänd F-skatt och momsregistrering</li><li>Ansvarsförsäkring</li>
          <li>Inga betalningsanmärkningar</li><li>Erfarenhet av relining sedan {esc(since)}</li></ul>
          <h2>Tjänster</h2>
          <ul><li>Relining av avloppsstammar</li><li>Rörinspektion med kamera</li><li>Avloppsspolning</li><li>Relining av gjutjärnsrör</li></ul>
          <h2>Relaterat</h2>
          <div class="pills">
            {city_link}
            <a href="/relining/">Relining i din kommun</a>
            <a href="/pris/">Priser 2026</a>
            <a href="/guider/vad-ar-relining/">Vad är relining?</a>
            <a href="/for-proffs/">Anslut ditt företag</a>
          </div>
          <h2>Fler firmor</h2><div class="pills">{neigh_links}</div>
          <div class="cta-band" style="margin-top:40px"><h2>Vill du ha offert från {esc(name)}?</h2>
            <p>Beskriv ditt projekt så matchar vi dig med lokala firmor, inklusive denna.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Få offerter</a></div>
        </div></div></section>'''
        write(path + "index.html", page(f"{name} – relining i {ort} | Reliningkoll",
          f"{name} utför relining i {ort}. Granskad för F-skatt och försäkring. Begär kostnadsfri offert via Reliningkoll.",
          path, body, crumb=[("Hem","/"),("Företag","/foretag/"),(name,path)],
          schema=json.dumps({"@context":"https://schema.org","@type":"LocalBusiness","name":name,
            "address":{"@type":"PostalAddress","addressLocality":ort,"addressRegion":lan,"addressCountry":"SE"},
            "areaServed":lan,"url":BASE+path}, ensure_ascii=False)))

# ---------------------------------------------------------------- offert / proffs / om / legal / 404
def build_pages():
    # offert
    body = f'''<section class="hero"><div class="wrap narrow">
      {crumb_html([("Hem","/"),("Få offerter","/offert/")])}
      <h1 class="h1">Få offerter på relining</h1>
      <p class="lead">Gratis, upp till tre offerter, tar under en minut. Vi matchar dig med lokala firmor i din kommun.</p></div></section>
      <section style="padding-top:0"><div class="wrap narrow"><div class="quote-card" style="max-width:640px;margin:0 auto">
      <form data-lead action="https://formsubmit.co/{FORM_EMAIL}" method="POST">
        <input type="hidden" name="_subject" value="Ny reliningförfrågan">
        <input type="hidden" name="_captcha" value="false">
        <div class="field"><label for="o-typ">Vad vill du ha hjälp med?</label>
          <select id="o-typ" name="typ" required><option value="">Välj</option>
          <option>Relining av avloppsrör</option><option>Relining villa</option><option>Relining bostadsrätt/BRF</option>
          <option>Relining av gjutjärnsrör</option><option>Avloppsspolning</option><option>Rörinspektion</option>
          <option>Vet inte, vill ha rådgivning</option></select></div>
        <div class="field"><label>Vilken typ av fastighet?</label>
          <div class="chips">
            <label class="chip"><input type="radio" name="fastighet" value="Villa" checked><span>Villa</span></label>
            <label class="chip"><input type="radio" name="fastighet" value="Bostadsrätt"><span>Bostadsrätt</span></label>
            <label class="chip"><input type="radio" name="fastighet" value="BRF/Fastighet"><span>BRF / fastighet</span></label>
          </div></div>
        <div class="field"><label for="o-post">Postnummer</label><input id="o-post" name="postnummer" inputmode="numeric" required placeholder="t.ex. 652 24"></div>
        <div class="field"><label for="o-tel">Telefon</label><input id="o-tel" name="telefon" type="tel" required placeholder="07x xxx xx xx"></div>
        <div class="field"><label for="o-mail">E-post</label><input id="o-mail" name="epost" type="email" required placeholder="namn@exempel.se"></div>
        <div class="field"><label for="o-tid">När vill du genomföra arbetet?</label>
          <select id="o-tid" name="tidsplan"><option>Så snart som möjligt</option><option>Inom 3 månader</option>
          <option>Om 3 till 6 månader</option><option>Bara prisuppgift just nu</option></select></div>
        <div class="field"><label for="o-med">Vill du beskriva något mer? (frivilligt)</label>
          <textarea id="o-med" name="meddelande" rows="3" placeholder="T.ex. återkommande stopp, uppmätt rörlängd, tidigare inspektion"></textarea></div>
        <button class="btn btn-dark btn-lg" type="submit" style="width:100%">Skicka förfrågan</button>
        <p class="form-note">Gratis och utan förpliktelse. Dina uppgifter delas med upp till tre firmor i ditt område.</p>
        <p class="form-msg" role="status" aria-live="polite"></p>
      </form></div>
      <div class="prose" style="margin-top:40px"><h2>Så hanterar vi din förfrågan</h2>
        <ol><li>Din förfrågan granskas manuellt så att den är seriös och komplett.</li>
        <li>Vi skickar den till upp till tre granskade firmor som arbetar i din kommun.</li>
        <li>Du kontaktas av firmorna och jämför offerter i lugn och ro.</li></ol>
        <div class="callout"><p>Du bestämmer helt själv om du vill gå vidare. Att ta emot offerter kostar ingenting och binder dig inte.</p></div></div>
      </div></section>'''
    write("/offert/index.html", page("Få offerter på relining gratis | Reliningkoll",
      "Fyll i ditt projekt och få upp till tre offerter på relining, avloppsspolning eller rörinspektion från lokala firmor. Gratis och utan förpliktelse.",
      "/offert/", body, crumb=[("Hem","/"),("Få offerter","/offert/")]))

    # for-proffs
    body = f'''<section class="hero"><div class="wrap narrow">
      {crumb_html([("Hem","/"),("För proffs","/for-proffs/")])}
      <h1 class="h1">Få fler reliningjobb</h1>
      <p class="lead">Ta emot manuellt granskade förfrågningar från villaägare, bostadsrättsföreningar och fastighetsägare i din kommun. Ingen bindningstid, betala bara för de leads du accepterar.</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="mailto:{FORM_EMAIL}?subject=Anslut%20mitt%20företag">Anslut ditt företag</a>
        <a class="btn btn-ghost btn-lg" href="/foretag/">Se anslutna företag</a></div></div></section>
      <section class="bg-card"><div class="wrap">
        <div class="sec-head rv"><h2>Varför ansluta sig?</h2></div>
        <div class="grid grid-3">
          <div class="card rv"><div class="num">1</div><h3>Granskade leads</h3><p>Varje förfrågan kontrolleras manuellt och innehåller fastighetstyp, omfattning och tidsplan. Inga köpta listor.</p></div>
          <div class="card rv"><div class="num">2</div><h3>Direkt i inkorgen</h3><p>Nya leads skickas till dig och du väljer själv vilka du vill ta del av. Acceptera eller hoppa över med ett klick.</p></div>
          <div class="card rv"><div class="num">3</div><h3>Gratis företagssida</h3><p>Varje ansluten firmor får en SEO-optimerad profilsida på Reliningkoll, utan kostnad.</p></div>
        </div>
      </div></section>
      <section><div class="wrap narrow"><div class="prose">
        <h2>Så fungerar det</h2>
        <ol><li>Du ansluter ditt företag och anger vilka kommuner du arbetar i.</li>
        <li>Vi skickar förfrågningar som matchar ditt område och din kompetens.</li>
        <li>Du väljer vilka leads du vill ta del av och betalar endast för dem du accepterar.</li></ol>
        <h2>Krav för att bli ansluten</h2>
        <ul><li>Godkänd F-skatt och momsregistrering</li><li>Giltig ansvarsförsäkring</li>
        <li>Inga betalningar hos Kronofogden</li><li>Erfarenhet av relining</li><li>Referenser och omdömen</li></ul>
        <div class="callout"><p>Ingen bindningstid, ingen månadsavgift och ingen startkostnad. Du betalar bara för de förfrågningar du väljer att ta del av.</p></div>
        <div class="cta-band"><h2>Redo att ta emot leads?</h2><p>Mejla oss och berätta vilka kommuner du arbetar i.</p>
          <a class="btn btn-primary btn-lg" href="mailto:{FORM_EMAIL}?subject=Anslut%20mitt%20företag">Anslut ditt företag</a></div>
      </div></div></section>'''
    write("/for-proffs/index.html", page("Få fler reliningjobb – anslut ditt företag | Reliningkoll",
      "Få manuellt granskade reliningleads i din kommun. Gratis att ansluta, ingen bindningstid, betala bara för leads du accepterar.",
      "/for-proffs/", body, crumb=[("Hem","/"),("För proffs","/for-proffs/")]))

    # om oss
    body = f'''<section class="hero"><div class="wrap narrow">
      {crumb_html([("Hem","/"),("Om oss","/om-oss/")])}
      <h1 class="h1">Om Reliningkoll</h1>
      <p class="lead">Vi gör det enkelt att jämföra relining och avloppsrenovering, och att hitta en trygg entreprenör i sin kommun.</p></div></section>
      <section style="padding-top:0"><div class="wrap narrow"><div class="prose">
        <h2>Vad vi gör</h2>
        <p>Reliningkoll är en oberoende jämförelsetjänst. Du beskriver ditt projekt en gång, och vi skickar förfrågan till upp till tre granskade entreprenörer som arbetar i din kommun. Tjänsten är kostnadsfri för dig som privatperson och du har ingen skyldighet att anlita någon.</p>
        <h2>Så tjänar vi pengar</h2>
        <p>Tjänsten är gratis för dig. De anslutna företagen betalar en avgift för de förfrågningar de väljer att ta del av. Vi tar aldrig provision på själva arbetet och påverkar inte vilket pris du får.</p>
        <h2>Så granskar vi företagen</h2>
        <ul><li>Godkänd F-skatt och momsregistrering</li><li>Ansvarsförsäkring</li>
        <li>Inga betalningar hos Kronofogden</li><li>Erfarenhet av relining</li><li>Kontinuerlig uppföljning av omdömen</li></ul>
        <h2>Kontakt</h2>
        <p>Mejla oss på <a href="mailto:{FORM_EMAIL}">{FORM_EMAIL}</a>. Vi svarar normalt inom en arbetsdag.</p>
      </div></div></section>'''
    write("/om-oss/index.html", page("Om Reliningkoll – oberoende jämförelse av relining",
      "Reliningkoll är en oberoende jämförelsetjänst för relining. Gratis för privatpersoner, granskade entreprenörer och inga provisioner.",
      "/om-oss/", body, crumb=[("Hem","/"),("Om oss","/om-oss/")]))

    # integritetspolicy
    body = f'''<section class="hero"><div class="wrap narrow">{crumb_html([("Hem","/"),("Integritetspolicy","/integritetspolicy/")])}
      <h1 class="h1">Integritetspolicy</h1></div></section>
      <section style="padding-top:0"><div class="wrap narrow"><div class="prose">
      <p>Vi värnar om din personliga integritet och behandlar dina uppgifter enligt dataskyddsförordningen (GDPR).</p>
      <h2>Vilka uppgifter vi samlar in</h2>
      <p>När du skickar en förfrågan samlar vi in namn, telefonnummer, e-post, postnummer och uppgifter om ditt projekt. Uppgifterna används för att matcha dig med entreprenörer som kan utföra arbetet.</p>
      <h2>Vem vi delar uppgifterna med</h2>
      <p>Vi delar dina uppgifter med upp till tre entreprenörer som arbetar i din kommun. Vi säljer aldrig dina uppgifter till tredje part utanför detta syfte.</p>
      <h2>Dina rättigheter</h2>
      <p>Du har rätt att begära utdrag, rättelse eller radering av dina uppgifter. Kontakta oss på <a href="mailto:{FORM_EMAIL}">{FORM_EMAIL}</a>.</p>
      <h2>Lagringstid</h2>
      <p>Vi sparar uppgifterna så länge de behövs för att hantera din förfrågan och därefter enligt gällande lagkrav.</p>
      </div></div></section>'''
    write("/integritetspolicy/index.html", page("Integritetspolicy | Reliningkoll",
      "Så behandlar Reliningkoll dina personuppgifter enligt GDPR. Vilka uppgifter vi samlar in, vem vi delar dem med och vilka rättigheter du har.", "/integritetspolicy/", body,
      crumb=[("Hem","/"),("Integritetspolicy","/integritetspolicy/")]))

    # villkor
    body = f'''<section class="hero"><div class="wrap narrow">{crumb_html([("Hem","/"),("Användarvillkor","/anvandarvillkor/")])}
      <h1 class="h1">Användarvillkor</h1></div></section>
      <section style="padding-top:0"><div class="wrap narrow"><div class="prose">
      <h2>Om tjänsten</h2>
      <p>Reliningkoll förmedlar kontakt mellan dig som privatperson och entreprenörer inom relining och avloppsrenovering. Tjänsten är kostnadsfri för dig och medför ingen köpförpliktelse.</p>
      <h2>Vårt ansvar</h2>
      <p>Vi förmedlar kontakt men är inte part i avtalet mellan dig och entreprenören. Vi ansvarar inte för utfört arbete, pris eller garanti. Kontrollera alltid att entreprenören har F-skatt och försäkring innan du beställer.</p>
      <h2>Företag som ansluter sig</h2>
      <p>Anslutna företag ansvarar för att lämnade uppgifter är korrekta och att arbetet utförs enligt branschregler.</p>
      <h2>Kontakt</h2>
      <p>Frågor om villkoren besvaras på <a href="mailto:{FORM_EMAIL}">{FORM_EMAIL}</a>.</p>
      </div></div></section>'''
    write("/anvandarvillkor/index.html", page("Användarvillkor | Reliningkoll",
      "Villkor för att använda Reliningkoll. Så fungerar förmedlingen, ditt ansvar och vårt när du begär offerter på relining eller avloppsrenovering.", "/anvandarvillkor/", body,
      crumb=[("Hem","/"),("Användarvillkor","/anvandarvillkor/")], noindex=False))

    # 404
    body = f'''<section class="hero center"><div class="wrap narrow">
      <h1 class="h1">Sidan hittades inte</h1>
      <p class="lead">Sidan du letar efter finns inte längre eller har flyttats. Prova startsidan eller prisguiden.</p>
      <div class="hero-cta" style="justify-content:center">
        <a class="btn btn-primary btn-lg" href="/">Till startsidan</a>
        <a class="btn btn-ghost btn-lg" href="/pris/">Priser</a></div>
      </div></section>'''
    write("/404.html", page("Sidan hittades inte | Reliningkoll", "Sidan kunde inte hittas.",
      "/404", body, noindex=True))

if __name__ == "__main__":
    build_prices()
    build_cities()
    build_firms()
    build_pages()
    print("del 2 klar")
