#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data-drivet geo-lager. Varje stads sida drivs av RIKTIG SCB-data:
bostadsbestånd per typ, hela byggnadsperiodfördelningen per årtionde, och befolkning.
Bara kommuner med verklig marknadsstorlek publiceras."""
import sys, os, json
sys.path.insert(0, "/home/clawd/reliningkoll")
import build_core as C
from build_core import page, crumb_html, write, esc, BASE, FORM_EMAIL
import build_muni as M

SCB = json.load(open("/home/clawd/reliningkoll/data/scb_bostad.json", encoding="utf-8"))
EXTRA = json.load(open("/home/clawd/reliningkoll/data/scb_extra.json", encoding="utf-8"))
_by_name = {v["namn"]: v for v in SCB.values()}

GEO = {}
for slug, name, lan, areas in M.ALL:
    d = _by_name.get(name)
    if not d:
        continue
    e = {}
    for kod, v in EXTRA.items():
        if v.get("kommun") == name:
            e = v
            break
    GEO[slug] = dict(d, slug=slug, name=name, lan=lan, areas=areas,
                     befolkning=e.get("befolkning"), period=e.get("period", {}))

CITY_SET = [s for s, d in GEO.items() if d["totalt"] >= 20000]
CITY_SET.sort(key=lambda s: -GEO[s]["totalt"])
TOP_SERVICE = CITY_SET[:10]  # endast orter med dokumenterad sokvolym

PERIODS = ["-1930", "1931-1940", "1941-1950", "1951-1960", "1961-1970",
           "1971-1980", "1981-1990", "1991-2000", "2001-2010", "2011-2020", "2021-"]
PKORT = {"-1930": "före 1930", "1931-1940": "1931–1940", "1941-1950": "1941–1950",
         "1951-1960": "1951–1960", "1961-1970": "1961–1970", "1971-1980": "1971–1980",
         "1981-1990": "1981–1990", "1991-2000": "1991–2000", "2001-2010": "2001–2010",
         "2011-2020": "2011–2020", "2021-": "2021 och senare"}

def fmt(n):
    return f"{n:,}".replace(",", " ")

def narr(d):
    if d["smahus_andel"] >= 50:
        return (f"{d['name']} är en kommun som domineras av småhus. {fmt(d['smahus'])} av "
                f"{fmt(d['totalt'])} bostäder är just småhus, vilket gör villaägare till den största "
                f"gruppen som behöver se över sina avloppsrör. I äldre villor är gjutjärnsrör regel.")
    if d["smahus_andel"] <= 25:
        return (f"{d['name']} är tät och domineras av flerbostadshus. {fmt(d['flerbost'])} av "
                f"{fmt(d['totalt'])} bostäder ligger i flerbostadshus, vilket gör relining av stammar "
                f"i bostadsrättsföreningar och fastighetsbolag till den vanligaste åtgärden här.")
    return (f"{d['name']} har en blandning av småhus och flerbostadshus: {fmt(d['smahus'])} småhus och "
            f"{fmt(d['flerbost'])} lägenheter i flerbostadshus. Både villaägare och "
            f"bostadsrättsföreningar har anledning att se över sina rör.")

def age(d):
    n = d["smahus_pre1950"]
    p = d["pre1970_andel"]
    if n >= 10000:
        return (f"I {d['name']} finns {fmt(n)} småhus byggda före 1950. Hus från den tiden byggdes "
                f"i regel med gjutjärnsrör, som efter decennier rostar inifrån och till slut ger "
                f"återkommande stopp. Det är den enskilt största gruppen fastigheter som kan behöva relining.")
    if n >= 3000:
        return (f"I {d['name']} finns {fmt(n)} småhus byggda före 1950, och totalt byggdes {p} procent "
                f"av alla bostäder före 1970. Många av dem har gjutjärnsrör som närmar sig eller har "
                f"passerat sin tekniska livslängd.")
    if n >= 1000:
        return (f"Före 1950 byggdes {fmt(n)} småhus i {d['name']}, och {p} procent av kommunens alla "
                f"bostäder tillkom före 1970. De äldsta av dem har gjutjärnsrör.")
    return (f"{p} procent av bostäderna i {d['name']} byggdes före 1970. Det äldre beståndet är mindre "
            f"än i storstäderna, men gjutjärnsrör förekommer i de äldsta husen även här.")

def period_table(d):
    sm = d.get("period", {}).get("SMÅHUS", {})
    fb = d.get("period", {}).get("FLERBOST", {})
    if not sm:
        return "", ""
    rows = ""
    for p in PERIODS:
        a, b = sm.get(p, 0), fb.get(p, 0)
        if a == 0 and b == 0:
            continue
        rows += f"<tr><td>{PKORT[p]}</td><td>{fmt(a)}</td><td>{fmt(b)}</td></tr>"
    tot = f"<tr><td><strong>Totalt</strong></td><td><strong>{fmt(d['smahus'])}</strong></td><td><strong>{fmt(d['flerbost'])}</strong></td></tr>"
    tbl = (f'<table class="tbl" style="margin-bottom:24px"><thead><tr><th>Byggnadsperiod</th>'
           f'<th>Småhus</th><th>Lägenheter i flerbostadshus</th></tr></thead><tbody>{rows}{tot}</tbody></table>'
           f'<p class="small" style="color:#5c6b69">Källa: SCB, bostadsbestånd per kommun och byggnadsperiod 2024.</p>')

    peak = max(sm, key=sm.get) if sm else None
    old = [p for p in PERIODS if sm.get(p, 0) > 0]
    narrative = ""
    if peak:
        narrative += (f"Flest småhus i {d['name']} byggdes under perioden {PKORT[peak]}, "
                      f"nämligen {fmt(sm[peak])} stycken. ")
    if old:
        narrative += (f"De äldsta småhusen härrör från tiden {PKORT[old[0]]}. ")
    narrative += (f"Rör läggs i samband med att huset byggs, så byggnadsperioderna berättar "
                  f"indirekt vilka rör kommunens hus har. Hus byggda fram till 1970 har i regel "
                  f"gjutjärnsrör; därefter blev plaströr vanligare.")
    return tbl, narrative

def build_cities_geo():
    cards = ''.join(f'<a class="pills" href="/relining/{s}/">{esc(GEO[s]["name"])}</a>' for s in CITY_SET)
    hub = f'''<section class="hero"><div class="wrap narrow">
      {crumb_html([("Hem","/"),("Hitta firmor","/relining/")])}
      <h1 class="h1">Relining i din kommun</h1>
      <p class="lead">Vi förmedlar lokala reliningfirmor. Välj din kommun för lokala fakta om bostadsbeståndet, byggnadsperioder, priser och entreprenörer i ditt område.</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få offerter</a></div>
    </div></section>
    <section class="s-pt0"><div class="wrap narrow"><div class="prose">
      <h2>Varför behovet skiljer sig mellan kommuner</h2>
      <p>Omfattningen av relining följer bostadsbeståndets ålder. I kommuner med mycket bebyggelse före 1970 är gjutjärnsrören vanliga, och där blir relining en vanlig åtgärd. I kommuner som vuxit senare dominerar plaströr, som åldras långsammare men kan bli spröda.</p>
      <p>Varje kommunsida här bygger på riktig statistik från SCB: antal bostäder, fördelning mellan småhus och flerbostadshus, och hur stor del som byggdes under varje årtionde. Statistiken berättar indirekt vilka rör kommunens hus har, eftersom rör läggs i samband med att huset byggs.</p>
      <h2>Så använder du sidorna</h2>
      <p>Börja med att titta på andelen bostäder byggda före 1970 i din kommun. En hög andel betyder att många fastigheter har rör som närmar sig eller passerat sin tekniska livslängd. Titta sedan på fördelningen mellan småhus och flerbostadshus: i en småhusdominerad kommun är det villaägaren som driver projekten, i en tät kommun är det oftare bostadsrättsföreningar och fastighetsbolag.</p>
      <h2>Från inspektion till offert</h2>
      <p>Oavsett kommun är vägen till rätt åtgärd densamma: en kamera inspektion visar rörens skick, och utifrån den går det att avgöra om spolning, relining eller rörbyte är rätt. Först därefter är en offert möjlig att jämföra på riktigt.</p>
      <div class="callout"><p>All statistik på dessa sidor kommer från SCB:s öppna API. Vi publicerar inga påhittade betyg eller recensioner.</p></div>
    </div></div></section>
    <section><div class="wrap"><div class="pills rv">{cards}</div></div></section>'''
    write("/relining/index.html", page("Relining i din kommun – lokala fakta och firmor | Reliningkoll",
      "Se bostadsbestånd, byggnadsperioder och lokala förutsättningar för relining i din kommun, byggda på riktig statistik från SCB. Välj kommun och jämför.",
      "/relining/", hub, crumb=[("Hem","/"),("Relining","/relining/")]))

    for slug in CITY_SET:
        d = GEO[slug]
        name, lan, areas = d["name"], d["lan"], d["areas"]
        path = f"/relining/{slug}/"
        ptbl, pnarr = period_table(d)
        bef = f"{fmt(d['befolkning'])} invånare" if d.get("befolkning") else ""
        if areas:
            omr2 = f"Förutom {esc(name)} förmedlar vi firmor i {esc(', '.join(areas))}."
        else:
            omr2 = f"Förutom {esc(name)} förmedlar vi firmor i närliggande orter i {esc(lan)}."
        _relh = f'<h2>Relaterat för {esc(name)}</h2>'
        _firm = '<a href="/foretag/">Så granskar vi firmor</a>'
        _guides = ('<a href="/guider/vad-ar-relining/">Vad är relining?</a>'
                   '<a href="/guider/relining-eller-stambyte/">Relining eller stambyte?</a>'
                   '<a href="/guider/hur-lange-haller-relining/">Hur länge håller relining?</a>'
                   '<a href="/pris/">Priser 2026</a>'
                   '<a href="/guider/">Alla guider</a>')
        _ci = CITY_SET.index(slug)
        _neighc = [CITY_SET[(_ci + k) % len(CITY_SET)] for k in range(1, 13)]
        _clinks = ''.join(f'<a href="/relining/{x}/">{esc(GEO[x]["name"])}</a>' for x in _neighc)
        rel_block = _relh + '<div class="pills">' + _firm + _guides + '</div>'
        rel_block += '<h2 style="font-size:22px">Relining i fler kommuner</h2><div class="pills rv">' + _clinks + '</div>'
        svc = (f'<h2>Spolning och rörinspektion i {esc(name)}</h2>'
               f'<p>Har du ett stopp eller behöver du inspektera rören? Se '
               f'<a href="/avloppsspolning/{slug}/">avloppsspolning i {esc(name)}</a> och '
               f'<a href="/rorinspektion/{slug}/">rörinspektion i {esc(name)}</a>.</p>'
               ) if slug in TOP_SERVICE else ""

        # extra sektion beroende pa bestand (ger olika sidstruktur)
        if d["smahus_andel"] <= 25:
            extra = (f'<h2>Relining i bostadsrätter och fastigheter i {esc(name)}</h2>'
                     f'<p>Med {fmt(d["flerbost"])} lägenheter i flerbostadshus är det i {esc(name)} '
                     f'ofta föreningar och fastighetsbolag som driver reliningprojekt. Arbetet läggs '
                     f'upp stam för stam så att boende bara berörs några dagar i taget, och föreningen '
                     f'får dokumentation och garanti på hela anläggningen.</p>')
        elif d["smahus_andel"] >= 50:
            extra = (f'<h2>Relining av villa i {esc(name)}</h2>'
                     f'<p>Med {fmt(d["smahus"])} småhus är villaägaren den vanligaste beställaren i '
                     f'{esc(name)}. I en villa ligger delar av ledningarna ofta åtkomliga i källare '
                     f'eller krypgrund, vilket gör arbetet snabbare, och du kan använda ROT-avdraget '
                     f'eftersom du äger och bor i huset.</p>')
        else:
            extra = (f'<h2>Både villa och bostadsrätt i {esc(name)}</h2>'
                     f'<p>{esc(name)} har både ett stort inslag av småhus och många lägenheter i '
                     f'flerbostadshus. Villaägare kan använda ROT-avdraget, medan föreningar driver '
                     f'sina projekt över underhållsplanen. Underlaget för offert är detsamma: en '
                     f'kamera inspektion av rören.</p>')

        body = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Relining","/relining/"),(name,path)])}
          <h1 class="h1">Relining i {esc(name)}</h1>
          <p class="lead">{esc(name)} har {bef} och {fmt(d['totalt'])} bostäder, varav {fmt(d['smahus'])} småhus. {d['pre1970_andel']} procent av bostäderna byggdes före 1970 – då gjutjärnsrör var standard. Vi matchar dig med upp till tre lokala firmor i {esc(lan)}.</p>
          <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få 3 offerter i {esc(name)}</a>
            <a class="btn btn-ghost btn-lg" href="/pris/">Se priser</a></div>
        </div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          <h2>Bostadsbeståndet i {esc(name)}</h2>
          <p>{narr(d)}</p>
          <table class="tbl" style="margin-bottom:24px"><thead><tr><th>Bostadstyp</th><th>Antal</th><th>Andel</th></tr></thead><tbody>
            <tr><td>Småhus</td><td>{fmt(d['smahus'])}</td><td>{d['smahus_andel']} %</td></tr>
            <tr><td>Lägenheter i flerbostadshus</td><td>{fmt(d['flerbost'])}</td><td>{100-d['smahus_andel']} %</td></tr>
            <tr><td><strong>Totalt</strong></td><td><strong>{fmt(d['totalt'])}</strong></td><td>100 %</td></tr>
            <tr><td>Varav småhus byggda före 1950</td><td>{fmt(d['smahus_pre1950'])}</td><td></td></tr>
            <tr><td>Varav byggda före 1970</td><td></td><td>{d['pre1970_andel']} %</td></tr>
          </tbody></table>
          <p class="small" style="color:#5c6b69">Källa: SCB, bostadsbestånd per kommun 2024.</p>
          <h2>När byggdes husen i {esc(name)}?</h2>
          {ptbl}
          <p>{pnarr}</p>
          <h2>Vad det betyder för avloppet i {esc(name)}</h2>
          <p>{age(d)}</p>
          <p>Rör som lagts före 1970 är oftast av gjutjärn. De rostar inifrån, bygger avlagringar och ger till slut återkommande stopp. Relining förnyar röret inifrån utan att golv, väggar eller trädgård behöver rivas.</p>
          {extra}
          <h2>Riktpriser i {esc(lan)}</h2>
          <p>För villa ligger komplett relining oftast mellan 80 000 och 250 000 kr, per meter rör 800–1 500 kr och en avloppsspolning 1 500–4 500 kr. <a href="/pris/">Se alla priser med räkneexempel</a>. I villa i {esc(name)} är arbetskostnaden ROT-berättigad, vilket ger 30 procent tillbaka upp till 50 000 kr per person och år.</p>
          <h2>Så går det till i {esc(name)}</h2>
          <ol><li>Du beskriver ditt projekt och ort.</li><li>Din förfrågan granskas och skickas till upp till tre firmor som arbetar i {esc(name)}.</li><li>Du får offerter och väljer själv om och med vem du går vidare.</li></ol>
          <h2>Täckningsområde</h2>
          <p>{omr2}</p>
          <h2>Vanliga frågor om relining i {esc(name)}</h2>
          <div class="faq">
            <details><summary>Hur många hus i {esc(name)} har gjutjärnsrör?</summary><p>{fmt(d['smahus_pre1950'])} småhus i {esc(name)} byggdes före 1950, och {d['pre1970_andel']} procent av kommunens bostäder tillkom före 1970. Hus från de åren byggdes i regel med gjutjärnsrör.</p></details>
            <details><summary>När byggdes de flesta husen i {esc(name)}?</summary><p>Flest småhus byggdes under perioden {PKORT.get(max(d.get('period',{}).get('SMÅHUS',{'-1930':1}), key=d.get('period',{}).get('SMÅHUS',{'-1930':1}).get), '-1930')}.</p></details>
            <details><summary>Vad kostar relining i {esc(name)}?</summary><p>För en villa ligger priset oftast mellan 80 000 och 250 000 kr före ROT-avdrag. Exakt pris beror på rörens längd, skick och åtkomst.</p></details>
            <details><summary>Kan jag använda ROT-avdraget i {esc(name)}?</summary><p>Ja, för relining i egen villa. Avdraget är 30 procent av arbetskostnaden, upp till 50 000 kr per person och år.</p></details>
          </div>
          {svc}
          {rel_block}
          <div class="cta-band" style="margin-top:40px"><h2>Få offerter på relining i {esc(name)}</h2>
            <p>Gratis, utan förpliktelse. Upp till tre lokala firmor.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Skicka förfrågan</a></div>
        </div></div></section>'''

        faq = [("Hur många hus i "+name+" har gjutjärnsrör?",
                f"{d['smahus_pre1950']} småhus byggdes före 1950 och {d['pre1970_andel']}% av bostäderna före 1970."),
               ("Vad kostar relining i "+name+"?",
                "För en villa ligger priset oftast mellan 80 000 och 250 000 kr före ROT-avdrag.")]
        write(path + "index.html", page(f"Relining {name} – bostadsbestånd, pris och firmor | Reliningkoll",
              f"Relining i {name}: {fmt(d['totalt'])} bostäder, {d['pre1970_andel']} procent byggda före 1970. Se kommunens bostadsbestånd, byggnadsperioder och lokala firmor.",
              path, body, faq=faq, crumb=[("Hem","/"),("Relining","/relining/"),(name,path)]))

def build_service_geo():
    cards = ''.join(f'<a class="pills" href="/avloppsspolning/{s}/">{esc(GEO[s]["name"])}</a>' for s in TOP_SERVICE)
    write("/avloppsspolning/index.html", page("Avloppsspolning – hitta spolfirma i din kommun | Reliningkoll",
      "Avloppsspolning nära dig. Jämför lokala spolfirmor, priser och vad som gäller vid stopp i avloppet — och när relining är rätt åtgärd i stället.",
      "/avloppsspolning/",
      f'''<section class="hero"><div class="wrap narrow">
        {crumb_html([("Hem","/"),("Avloppsspolning","/avloppsspolning/")])}
        <h1 class="h1">Avloppsspolning i hela Sverige</h1>
        <p class="lead">Stopp i avloppet? Vi förmedlar lokala spolfirmor som löser stopp med högtryck och kamera.</p>
        <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få hjälp med stopp</a>
          <a class="btn btn-ghost btn-lg" href="/pris/avloppsspolning/">Se priser</a></div></div></section>
        <section class="s-pt0"><div class="wrap narrow"><div class="prose">
          <h2>Vad som orsakar stopp i avloppet</h2>
          <p>Ett stopp kommer sällan av en slump. I köket är det fett och matrester som stelnar och bygger beläggning. I badrummet är det hår som blandas med tvålrester. I äldre gjutjärnsrör gör den rostiga insidan att allt fastnar lättare, och proppen blir tätare för varje gång.</p>
          <h2>Vad du kan lösa själv</h2>
          <p>Ett enkelt stopp går ofta att lösa med vaskrensare, kokhett vatten eller genom att skruva loss och rengöra vattenlåset. Undvik starka kemiska avloppsrens, som kan skada äldre gjutjärnsrör och täta ledningar.</p>
          <h2>När du bör anlita en spolfirma</h2>
          <p>Sitter stoppet längre in än vattenlåset, påverkar flera avlopp samtidigt, eller återkommer det snabbt, krävs högtrycksspolning. Då används rätt tryck och dyse för rörets dimension, och ofta en kamera för att se orsaken. Är rören slitna invändigt kommer stoppet att återkomma tills röret åtgärdas — då är relining ofta rätt lösning.</p>
          <h2>Vad spolning kostar</h2>
          <p>En rensning av en enkel propp ligger vanligen mellan 800 och 1 800 kr. Högtrycksspolning i villa kostar oftast 1 500 till 3 500 kr, medan en fastighet med flera stammar landar mellan 3 000 och 6 000 kr. Akut utryckning kväll eller helg kan kosta 2 000 till 5 000 kr.</p>
          <h2>Akut eller planerat</h2>
          <p>Ett akut stopp mitt i natten kostar mer än en planerad spolning. Har du äldre rör och vet med dig att stopp återkommer är det billigare att boka förebyggande spolning i tid än att vänta på nästa översvämning. Be samtidigt om en kamera inspektion när firman ändå är på plats.</p>
          <h2>Så undviker du återkommande stopp</h2>
          <ul><li>Häll aldrig fett i avloppet, oavsett rörtyp.</li>
          <li>Använd sil i vask och dusch.</li>
          <li>Spola förebyggande vartannat till var femte år vid äldre rör.</li>
          <li>Inspektera rören om stoppet återkommer mer än en gång per år.</li></ul>
        </div></div></section>
        <section><div class="wrap"><div class="pills rv">{cards}</div></div></section>''',
      crumb=[("Hem","/"),("Avloppsspolning","/avloppsspolning/")]))

    cards2 = ''.join(f'<a class="pills" href="/rorinspektion/{s}/">{esc(GEO[s]["name"])}</a>' for s in TOP_SERVICE)
    write("/rorinspektion/index.html", page("Rörinspektion – kamera inspektion av avlopp | Reliningkoll",
      "Rörinspektion med kamera i din kommun. Se rörens skick innan du beställer åtgärd, jämför lokala firmor och läs vad en inspektion kostar.",
      "/rorinspektion/",
      f'''<section class="hero"><div class="wrap narrow">
        {crumb_html([("Hem","/"),("Rörinspektion","/rorinspektion/")])}
        <h1 class="h1">Rörinspektion i hela Sverige</h1>
        <p class="lead">En kamera inspektion visar rörens skick innan du beställer åtgärd.</p>
        <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Boka inspektion</a>
          <a class="btn btn-ghost btn-lg" href="/pris/rorinspektion/">Se priser</a></div></div></section>
        <section class="s-pt0"><div class="wrap narrow"><div class="prose">
          <h2>Vad en kamera inspektion visar</h2>
          <p>En rörinspektion går ut på att en kamera förs genom ledningen och filmar insidan. Du får se rörens material och dimension, sprickor, fogar, avlagringar, rötter och var ett eventuellt problem sitter. Det är den enda tillförlitliga metoden för att bedöma rörens skick.</p>
          <h2>Varför inspektionen alltid kommer först</h2>
          <p>Utan inspektion är varje offert på relining en gissning. Rörens längd, dimension och skick avgör både metod och pris, och en firma som lämnar pris utan att ha sett rören tar antingen för högt betalt eller riskerar att behöva lägga till i efterhand.</p>
          <h2>När du bör beställa inspektion</h2>
          <ul><li>Återkommande stopp trots spolning.</li>
          <li>Dålig lukt eller missfärgat vatten från avloppet.</li>
          <li>Innan du beställer relining eller stambyte.</li>
          <li>Inför köp av ett hus byggt före 1970.</li></ul>
          <h2>Vad rapporten ska innehålla</h2>
          <p>Du bör få filmen och ett protokoll med positionsangivelser, noterade skador och en rekommendation av åtgärd. Spara dokumentationen — den är underlag både för offerter och för framtida underhåll och försäljning.</p>
          <h2>Inspektion eller besiktning?</h2>
          <p>En rörinspektion med kamera visar rörens invändiga skick och är den åtgärd du beställer när du misstänker ett problem eller planerar relining. En avloppsbesiktning vid husköp är bredare och omfattar även brunnar, täthet och anslutningar. Båda bygger på samma kamerateknik, men beställs av olika skäl.</p>
          <h2>Så bokar du</h2>
          <p>Beskriv ditt ärende och din ort i formuläret, så förmedlar vi kontakt med lokala firmor som utför inspektion i din kommun. Du får film och protokoll, och kan därefter begära offert på den åtgärd inspektionen visar behövs — eller konstatera att rören är hela och att spolning räcker.</p>
          <div class="callout"><p>Inspektionen är grunden för alla seriösa offerter på relining. Utan den går det inte att veta rörens dimension, längd eller skick.</p></div>
        </div></div></section>
        <section><div class="wrap"><div class="pills rv">{cards2}</div></div></section>''',
      crumb=[("Hem","/"),("Rörinspektion","/rorinspektion/")]))

    for slug in TOP_SERVICE:
        d = GEO[slug]
        name, lan = d["name"], d["lan"]
        _ti = TOP_SERVICE.index(slug)
        alt = [TOP_SERVICE[(_ti + k) % len(TOP_SERVICE)] for k in range(1, 11)]
        links = ''.join(f'<a class="pills" href="/avloppsspolning/{s}/">{esc(GEO[s]["name"])}</a>' for s in alt)
        sm = d.get("period", {}).get("SMÅHUS", {})
        peak = max(sm, key=sm.get) if sm else None
        peak_txt = f" Flest hus byggdes {PKORT.get(peak, '')}, vilket ger en stor andel rör från den tiden." if peak else ""

        p = f"/avloppsspolning/{slug}/"
        b = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Avloppsspolning","/avloppsspolning/"),(name,p)])}
          <h1 class="h1">Avloppsspolning i {esc(name)}</h1>
          <p class="lead">Stopp i avloppet i {esc(name)}? Kommunen har {fmt(d['totalt'])} bostäder och {d['pre1970_andel']} procent av dem byggdes före 1970. Vi förmedlar lokala spolfirmor i {esc(lan)}.</p>
          <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få hjälp med stoppet</a>
            <a class="btn btn-ghost btn-lg" href="/pris/avloppsspolning/">Se priser</a></div></div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          <h2>Stopp i avloppet i {esc(name)}</h2>
          <p>I {esc(name)} byggdes {d['pre1970_andel']} procent av bostäderna före 1970.{peak_txt} I äldre gjutjärnsrör bygger rost och avlagringar upp en beläggning invändigt, och då räcker det med lite fett eller hår för att det ska bli stopp. Är stoppet återkommande är det oftast rören – inte proppen – som är problemet.</p>
          <h2>Riktpriser i {esc(lan)}</h2>
          <table class="tbl" style="margin-bottom:24px"><thead><tr><th>Åtgärd</th><th>Riktpris</th></tr></thead><tbody>
            <tr><td>Rensning, enkel propp</td><td>800 – 1 800 kr</td></tr>
            <tr><td>Högtrycksspolning villa</td><td>1 500 – 3 500 kr</td></tr>
            <tr><td>Spolning flerbostadshus</td><td>3 000 – 6 000 kr</td></tr>
            <tr><td>Akut kväll/helg</td><td>2 000 – 5 000 kr</td></tr>
            <tr><td>Rörinspektion med kamera</td><td>0 – 2 500 kr</td></tr>
          </tbody></table>
          <div class="callout"><p>Återkommer stoppet är orsaken oftast avlagringar eller rötter. Då ger en rörinspektion svaret, och relining kan vara rätt lösning på sikt.</p></div>
          <h2>Relining i {esc(name)}</h2>
          <p>Om stoppet beror på slitna rör kan relining vara ett billigare alternativ än att spola om och om igen. Läs mer om <a href="/relining/{slug}/">relining i {esc(name)}</a>.</p>
          <h2>Vanliga frågor om stopp i {esc(name)}</h2>
          <div class="faq">
            <details><summary>Vad kostar avloppsspolning i {esc(name)}?</summary><p>En spolning ligger vanligen mellan 1 500 och 3 500 kr. Akut kväll eller helg kan kosta mer.</p></details>
            <details><summary>Kommer stoppet tillbaka?</summary><p>Är orsaken avlagringar eller rötter kommer stoppet ofta tillbaka. Då är rörinspektion och eventuell relining rätt åtgärd.</p></details>
          </div>
          <h2 style="font-size:22px">Avloppsspolning i fler orter</h2>
          <div class="pills rv">{links}</div>
          <div class="cta-band" style="margin-top:40px"><h2>Få hjälp med stoppet i {esc(name)}</h2>
            <p>Gratis och utan förpliktelse. Lokala firmor i {esc(lan)}.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Skicka förfrågan</a></div>
        </div></div></section>'''
        write(p+"index.html", page(f"Avloppsspolning {esc(name)} – pris och lokala firmor | Reliningkoll",
          f"Avloppsspolning i {name}? Hitta lokala spolfirmor i {lan}. {d['pre1970_andel']}% av bostäderna byggda före 1970. Priser för stopp i avloppet.",
          p, b, crumb=[("Hem","/"),("Avloppsspolning","/avloppsspolning/"),(name,p)]))

        alt2 = [TOP_SERVICE[(_ti + k) % len(TOP_SERVICE)] for k in range(1, 11)]
        _sm2 = d.get("period", {}).get("SMÅHUS", {})
        _peak2 = max(_sm2, key=_sm2.get) if _sm2 else None
        links2 = ''.join(f'<a class="pills" href="/rorinspektion/{s}/">{esc(GEO[s]["name"])}</a>' for s in alt2)
        p2 = f"/rorinspektion/{slug}/"
        b2 = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Rörinspektion","/rorinspektion/"),(name,p2)])}
          <h1 class="h1">Rörinspektion i {esc(name)}</h1>
          <p class="lead">Beställ kamera inspektion av avloppsrör i {esc(name)}. Vi förmedlar lokala firmor i {esc(lan)} som dokumenterar rörens skick.</p>
          <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Boka inspektion</a>
            <a class="btn btn-ghost btn-lg" href="/pris/rorinspektion/">Se priser</a></div></div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          <h2>Vad en rörinspektion visar</h2>
          <p>Med en kamera inspekteras rören inifrån i {esc(name)}. Du ser rörens skick, dimension, eventuella sprickor, rötter och avlagringar. I en kommun där {d['pre1970_andel']} procent av bostäderna byggdes före 1970 är det särskilt relevant att veta om rören är gjutjärn och hur de mår. Inspektionen är grunden för varje seriös offert.</p>
          <h2>Bostadsbeståndet i {esc(name)}</h2>
          <p>{narr(d)}</p>
          <p>{esc(name)} har {fmt(d['totalt'])} bostäder, varav {fmt(d['smahus'])} småhus och {fmt(d['flerbost'])} lägenheter i flerbostadshus. {d['pre1970_andel']} procent av bostäderna byggdes före 1970, och flest småhus tillkom under perioden {PKORT.get(_peak2, '')}.</p>
          <p>{age(d)} Det gör en kamera inspektion särskilt relevant här: den avgör om rören är gjutjärn, hur de mår och vilken åtgärd som är rimlig.</p>
          <h2>Riktpriser i {esc(lan)}</h2>
          <table class="tbl" style="margin-bottom:24px"><thead><tr><th>Tjänst</th><th>Riktpris</th></tr></thead><tbody>
            <tr><td>Inspektion villa</td><td>0 – 2 500 kr</td></tr>
            <tr><td>Inspektion fastighet</td><td>5 000 – 40 000 kr</td></tr>
            <tr><td>I samband med relining</td><td>Ofta inkluderad</td></tr>
          </tbody></table>
          <h2>När du bör beställa inspektion i {esc(name)}</h2>
          <ul><li>Återkommande stopp trots spolning</li><li>Dålig lukt eller missfärgat vatten</li>
          <li>Innan du beställer relining eller stambyte</li><li>Inför köp av äldre hus</li></ul>
          <h2>Relining i {esc(name)}</h2>
          <p>Visar inspektionen att rören är slitna men hela är relining ofta rätt åtgärd. Läs mer om <a href="/relining/{slug}/">relining i {esc(name)}</a>.</p>
          <h2 style="font-size:22px">Rörinspektion i fler orter</h2>
          <div class="pills rv">{links2}</div>
          <div class="cta-band" style="margin-top:40px"><h2>Boka rörinspektion i {esc(name)}</h2>
            <p>Kostnadsfri bedömning av lokala firmor i {esc(lan)}.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Skicka förfrågan</a></div>
        </div></div></section>'''
        write(p2+"index.html", page(f"Rörinspektion {esc(name)} – kamera inspektion av avlopp | Reliningkoll",
          f"Rörinspektion i {name} med kamera. Hitta lokala firmor i {lan}, se priser och vad inspektionen visar innan du beställer relining.",
          p2, b2, crumb=[("Hem","/"),("Rörinspektion","/rorinspektion/"),(name,p2)]))

if __name__ == "__main__":
    print("Kommuner med egen sida:", len(CITY_SET))
    print("Tjänsteorter:", len(TOP_SERVICE))
