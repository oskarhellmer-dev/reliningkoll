#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, json, datetime
sys.path.insert(0, "/home/clawd/reliningkoll")
import build_core as C
from build_extra import SUMMARY, CHECK
from build_core import page, crumb_html, write, esc, logo_ph, BASE, FORM_EMAIL

# ---------------------------------------------------------------- städer
# (slug, namn, län, områden)  — verkliga grannorter/stadsdelar
CITIES = [
 ("stockholm","Stockholm","Stockholms län",["Bromma","Södermalm","Östermalm","Vasastan","Solna","Nacka"]),
 ("goteborg","Göteborg","Västra Götalands län",["Majorna","Hisingen","Mölndal","Partille","Kungälv","Lerum"]),
 ("malmo","Malmö","Skåne län",["Limhamn","Rosengård","Husie","Bunkeflo","Lund","Trelleborg"]),
 ("uppsala","Uppsala","Uppsala län",["Gottsunda","Fålhagen","Sävja","Knivsta","Enköping"]),
 ("vasteras","Västerås","Västmanlands län",["Bäckby","Vallby","Kungsängen","Hallstahammar","Köping"]),
 ("orebro","Örebro","Örebro län",["Vivalla","Baronbackarna","Adolfsberg","Kumla","Hallsberg"]),
 ("linkoping","Linköping","Östergötlands län",["Ryd","Lambohov","Berga","Mjölby","Norrköping"]),
 ("norrkoping","Norrköping","Östergötlands län",["Haga","Klockaretorpet","Vilbergen","Finspång","Söderköping"]),
 ("jonkoping","Jönköping","Jönköpings län",["Huskvarna","Gränna","Bankeryd","Vaggeryd","Nässjö"]),
 ("helsingborg","Helsingborg","Skåne län",["Råå","Drottninghög","Högasten","Ängelholm","Höganäs"]),
 ("sundsvall","Sundsvall","Västernorrlands län",["Birsta","Nacksta","Sidsjö","Timrå","Härnösand"]),
 ("umea","Umeå","Västerbottens län",["Ålidhem","Ersboda","Teg","Holmsund","Vännäs"]),
 ("gavle","Gävle","Gävleborgs län",["Brynäs","Sätra","Bomhus","Sandviken","Valbo"]),
 ("boras","Borås","Västra Götalands län",["Norrby","Hässleholmen","Sjöbo","Ulricehamn","Alingsås"]),
 ("sodertalje","Södertälje","Stockholms län",["Hovsjö","Ronna","Fornhöjden","Nykvarn","Järna"]),
 ("eskilstuna","Eskilstuna","Södermanlands län",["Nyfors","Skiftinge","Torshälla","Strängnäs","Kungsör"]),
 ("halmstad","Halmstad","Hallands län",["Andersberg","Vallås","Fyllinge","Laholm","Oskarström"]),
 ("vaxjo","Växjö","Kronobergs län",["Araby","Teleborg","Hovshaga","Alvesta","Ljungby"]),
 ("karlstad","Karlstad","Värmlands län",["Våxnäs","Kronoparken","Hagaborg","Hammarö","Kristinehamn"]),
 ("falun","Falun","Dalarnas län",["Hälsinggården","Boosjö","Södra Hosjö","Borlänge","Säter"]),
 ("borlange","Borlänge","Dalarnas län",["Jakobsgårdarna","Tjärna Ängar","Kvarnsveden","Falun","Ludvika"]),
 ("solna","Solna","Stockholms län",["Råsunda","Hagalund","Bergshamra","Sundbyberg","Vasastan"]),
 ("lund","Lund","Skåne län",["Klostergården","Norra Fäladen","Linero","Staffanstorp","Dalby"]),
 ("nacka","Nacka","Stockholms län",["Saltsjöbaden","Orminge","Boo","Värmdö","Älta"]),
 ("huddinge","Huddinge","Stockholms län",["Flemingsberg","Skogås","Trångsund","Botkyrka","Södertörn"]),
 ("taby","Täby","Stockholms län",["Näsbypark","Roslags-Näsby","Gribbylund","Danderyd","Vallentuna"]),
 ("jarfalla","Järfälla","Stockholms län",["Barkarby","Kallhäll","Jakobsberg","Spånga","Upplands-Bro"]),
 ("ostersund","Östersund","Jämtlands län",["Odenskog","Lugnvik","Torvalla","Frösön","Åre"]),
 ("lulea","Luleå","Norrbottens län",["Bergnäset","Porsön","Kallkällan","Boden","Gammelstad"]),
 ("trollhattan","Trollhättan","Västra Götalands län",["Kronogården","Hjulkvarn","Lextorp","Vänersborg","Uddevalla"]),
 ("uddevalla","Uddevalla","Västra Götalands län",["Dalaberg","Hovhult","Skogslyckan","Lysekil","Munkedal"]),
 ("skovde","Skövde","Västra Götalands län",["Södermalm","Norrmalm","Käpplunda","Tibro","Mariestad"]),
 ("karlskrona","Karlskrona","Blekinge län",["Ronneby","Lyckeby","Hästö","Karlshamn","Olofström"]),
 ("nykoping","Nyköping","Södermanlands län",["Arnö","Harg","Brandkärr","Oxelösund","Trosa"]),
 ("kalmar","Kalmar","Kalmar län",["Berga","Norrliden","Funkabo","Nybro","Emmaboda"]),
 ("kristianstad","Kristianstad","Skåne län",["Gamlegården","Näsby","Åhus","Hässleholm","Bromölla"]),
 ("varberg","Varberg","Hallands län",["Håsten","Breared","Träslövsläge","Falkenberg","Kungsbacka"]),
 ("landskrona","Landskrona","Skåne län",["Borstahusen","Häljarp","Glumslöv","Svalöv","Eslöv"]),
 ("trelleborg","Trelleborg","Skåne län",["Klagstorp","Anderslöv","Skegrie","Vellinge","Ystad"]),
 ("sandviken","Sandviken","Gävleborgs län",["Barrsätra","Hedgrind","Högbo","Gävle","Hofors"]),
 ("enkoping","Enköping","Uppsala län",["Romberga","Lillkyrka","Fanna","Bålsta","Kungsängen"]),
 ("koping","Köping","Västmanlands län",["Västra","Östra","Kolsva","Arboga","Kungsör"]),
 ("katrineholm","Katrineholm","Södermanlands län",["Valla","Backa","Nyhem","Flen","Vingåker"]),
 ("motala","Motala","Östergötlands län",["Brinken","Klockrike","Varamon","Vadstena","Mjölby"]),
 ("skelleftea","Skellefteå","Västerbottens län",["Sörböle","Anderstorp","Kåge","Bureå","Byske"]),
 ("pitea","Piteå","Norrbottens län",["Hortlax","Rosvik","Norrfjärden","Älvsbyn","Luleå"]),
 ("ornskoldsvik","Örnsköldsvik","Västernorrlands län",["Sörliden","Bonäset","Gullänget","Kramfors","Sollefteå"]),
 ("kungsbacka","Kungsbacka","Hallands län",["Onsala","Åsa","Fjärås","Varberg","Mölndal"]),
 ("sigtuna","Sigtuna","Stockholms län",["Märsta","Rosersberg","Upplands-Väsby","Bålsta","Knivsta"]),
 ("vastervik","Västervik","Kalmar län",["Överum","Gamleby","Ankarsrum","Oskarshamn","Vimmerby"]),
]

# Ersätts av hela Sveriges 290 kommuner
from build_muni import ALL as CITIES

# ---------------------------------------------------------------- guider
def sec(h, ps):
    return f'<h2>{h}</h2>' + ''.join(f'<p>{p}</p>' for p in ps)
def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

GUIDES = {
 "vad-ar-relining": {
  "h1":"Vad är relining? Metoden förklaras enkelt",
  "title":"Vad är relining? Så fungerar metoden (guide 2026) | Reliningkoll",
  "desc":"Relining förnyar avloppsrör inifrån utan att golv och väggar rivs. Här förklarar vi hur metoden fungerar, när den passar och vad den kostar.",
  "body": sec("Relining i korthet", [
    "Relining är ett samlingsnamn för metoder som förnyar insidan av befintliga avloppsrör. I stället för att byta ut rören monterar man ett nytt rör inuti det gamla. Resultatet blir ett skarvfritt, tätt rör med ny livslängd, utan att golv, väggar eller trädgård behöver rivas upp.",
    "Metoden är särskilt vanlig i hus med gjutjärnsrör från 1900-talet, där rören rostat och fått avlagringar inifrån. I stället för ett fullt stambyte, som kan ta veckor och kräva att du flyttar ut, tar en relining oftast tre till fem arbetsdagar."]),
  "body2": sec("Så går det till, steg för steg", [
    "Arbetet börjar alltid med en rörinspektion. Med en kamera dokumenteras rörens skick, dimensioner och eventuella hinder. Utifrån det bedömer entreprenören vilken metod som passar."]) + ul([
    "Rören rengörs med högtryck och slits ned så att fodret fäster.",
    "Ett foder, oftast glasfiber eller polyester impregnerat med epoxi, förs in i röret.",
    "Fodret blåses upp så att det trycks mot rörväggen.",
    "Fodret härdas, antingen med varmt vatten, ånga eller UV-ljus.",
    "Anslutningar, golvbrunnar och grenrör öppnas och tätas.",
    "En ny kamera inspektion dokumenterar det färdiga resultatet."]) + sec("När passar relining?", [
    "Relining är ett bra val när rören är slitna men strukturellt hela, och när du vill slippa omfattande rivning. Det passar villor, bostadsrätter, bostadsrättsföreningar och kommersiella fastigheter.",
    "Är rören däremot kollapsade, fel dimensionerade eller om underlaget rör sig kraftigt kan ett byte vara enda lösningen. Läs mer i guiden om nackdelar med relining."]),
  "faq":[("Vad är skillnaden mellan relining och stambyte?","Relining renoverar rören inifrån utan att bygga om. Ett stambyte innebär att de gamla rören rivs ut och ersätts helt, vilket är mer ingripande och ofta dyrare."),
         ("Behöver jag flytta ut under arbetet?","Oftast inte. Relining görs skoningslöst mot bostaden och tar några få dagar. Vid stambyte behöver du normalt flytta ut."),
         ("Kan relining göras på gjutjärnsrör?","Ja. Det är en av de vanligaste situationerna. Rören rensas och slipas ned innan fodret installeras.")],
 },
 "relining-eller-stambyte": {
  "h1":"Relining eller stambyte? Så väljer du rätt",
  "title":"Relining eller stambyte? Pris, tid och skillnad 2026 | Reliningkoll",
  "desc":"Relining eller stambyte? Vi jämför kostnad, tid, livslängd och ingrepp så att du kan avgöra vilket som passar din fastighet.",
  "body": sec("Den viktigaste skillnaden", [
    "Stambyte betyder att de gamla rören rivs ut helt och ersätts med nya. Relining innebär att ett nytt rör byggs inuti det befintliga. Båda ger täta, moderna rör, men de skiljer sig kraftigt i ingrepp, tid och kostnad."]) +
    '<table class="tbl"><thead><tr><th>Aspekt</th><th>Relining</th><th>Stambyte</th></tr></thead><tbody>' +
    '<tr><td>Tid</td><td>3 till 5 dagar</td><td>Veckor till månader</td></tr>' +
    '<tr><td>Rivning</td><td>Ingen</td><td>Golv, väggar, schakt</td></tr>' +
    '<tr><td>Kostnad villa</td><td>80 000 – 250 000 kr</td><td>Ofta 25 till 50 % mer</td></tr>' +
    '<tr><td>Bo kvar</td><td>Ja, oftast</td><td>Nej, evakuering</td></tr>' +
    '<tr><td>Livslängd</td><td>40 till 50 år</td><td>50 år och uppåt</td></tr>' +
    '</tbody></table>' + sec("När relining vinner", [
    "Relining är oftast rätt val när rören blivit slitna men fortfarande är hela, och när ekonomin eller praktiska skäl gör ett fullt stambyte svårt. Du slipper riva badrum, kök och golv, och de boende kan vanligen stanna hemma."]) +
    sec("När stambyte är nödvändigt", [
    "Är rören kollapsade, har fall förlorats eller rör sig byggnaden kraftigt kan relining vara omöjligt eller kortsiktigt. Då är ett byte den hållbara lösningen. En rörinspektion avgör vilket som gäller för just din fastighet."]),
  "faq":[("Är relining billigare än stambyte?","Normalt ja, särskilt för villor, eftersom arbetet kräver så lite rivning. Skillnaden kan handla om 25 till 50 procent."),
         ("Kan man byta rör senare om man relinat?","Ja, men det innebär att det gamla systemet ändå måste tas bort. Relining är en långsiktig lösning, inte en tillfällig lapp.")],
 },
 "nackdelar-med-relining": {
  "h1":"Nackdelar med relining: tio saker att känna till",
  "title":"Nackdelar med relining – när metoden inte passar | Reliningkoll",
  "desc":"Relining är inte alltid rätt. Här är nackdelarna: trängre rördimension, begränsningar och situationer där stambyte ändå är bättre.",
  "body": sec("Relining är bra, men inte gratis eller perfekt", [
    "Relining löser många problem, men det finns verkliga begränsningar. Den som vill fatta ett bra beslut bör känna till dem innan offerterna beställs."]) + ul([
    "<strong>Röret blir trängre.</strong> Fodret minskar innerdiametern något, vilket i sällsynta fall kan påverka flödet i hårt belastade system.",
    "<strong>Kräver att röret är helt.</strong> Är röret kollapsat eller har tappat fall går det inte att relaina.",
    "<strong>Inte alltid godkänt i äldre miljöer.</strong> Vissa försäkringsbolag och myndigheter ställer krav på dokumentation.",
    "<strong>Kan dölja problem.</strong> Rötter och skador utanför röret åtgärdas inte av relining.",
    "<strong>Man blir bunden till leverantören.</strong> Framtida anslutningar kan kräva samma system.",
    "<strong>Priset varierar kraftigt.</strong> Låg offert kan sakna arbetsmoment som tillval.",
    "<strong>Ingen lösning vid fuktproblem eller sättningar.</strong> Då är orsaken utanför röret.",
    "<strong>De gamla rören är kvar.</strong> Fullt stambyte ger ett helt nytt system.",
    "<strong>Kvaliteten hänger på utförandet.</strong> Slarvig härdning förkortar livslängden.",
    "<strong>Inte alltid rätt i BRF-sammanhang.</strong> Styrelsen måste bedöma helheten, inte bara priset."]) +
    sec("Så undviker du fallgroparna", [
    "Kräv alltid en kamera inspektion före offert, skriftlig beskrivning av vad som ingår, uppgift om vilket system som används och vilken garanti som lämnas. Jämför minst tre offerter så att du ser vad som skiljer."]),
  "faq":[("Kan relining misslyckas?","Ja, vid slarvig rengöring eller felaktig härdning. Därför är dokumentation och garanti viktiga delar av offerten."),
         ("Höjer relining fastighetens värde?","Renoverade, täta rör är en fördel vid försäljning, särskilt om arbetet är dokumenterat.")],
 },
 "hur-lange-haller-relining": {
  "h1":"Hur länge håller relining?",
  "title":"Hur länge håller relining? Livslängd och garanti | Reliningkoll",
  "desc":"En korrekt utförd relining håller 40 till 50 år. Här är vad som avgör livslängden, hur garantier brukar se ut och vad du bör kräva skriftligt.",
  "body": sec("Svaret: normalt 40 till 50 år", [
    "Relining utförd enligt branschregler håller i 40 till 50 år, jämförbart med nya rör. Det förutsätter att rören var i tillräckligt gott skick för metoden och att jobbet dokumenterades ordentligt."]) +
    sec("Vad påverkar livslängden?", []) + ul([
    "Rörsystemets skick före arbetet.",
    "Val av foder och härdmetod.",
    "Hantverkarens erfarenhet och rutiner.",
    "Belastningen i systemet, till exempel antal boende.",
    "Vilka kemikalier som spolas ned i avloppet.",
    "Att anslutningar och golvbrunnar tätades korrekt."]) +
    sec("Garantier du bör kräva", [
    "Branschen lämnar normalt tio års garanti på utförandet, ibland längre. Be alltid om garantin skriftligt, tillsammans med dokumentationen av rörinspektionen före och efter arbetet."]),
  "faq":[("Håller relining lika länge som nya rör?","Ja, jämförbara rör håller 50 år och uppåt. Relining lämnar ofta något kortare teknisk livslängd, vilket brukar anges som 40 till 50 år."),
         ("Vad händer efter garantitiden?","Systemet fortsätter fungera men underhållsansvaret ligger på dig som fastighetsägare.")],
 },
 "strumpmetoden": {
  "h1":"Strumpmetoden: så fungerar den vanligaste reliningmetoden",
  "title":"Strumpmetoden (CIPP) – så fungerar relining steg för steg | Reliningkoll",
  "desc":"Strumpmetoden, även kallad CIPP, är den vanligaste reliningmetoden. Här är hela förloppet steg för steg och vad du bör kontrollera.",
  "body": sec("Vad strumpmetoden är", [
    "Strumpmetoden, internationellt CIPP, innebär att en flexibel slang av glasfiber eller polyester mättad med härdplast trycks in i det gamla röret, blåses upp mot rörväggen och härdas på plats. Resultatet är ett nytt, skarvfritt rör inuti det gamla."]) +
    sec("Förloppet steg för steg", []) + ul([
    "Rören högtrycksspolas och gammal beläggning slipas bort.",
    "Strumpan mättas med härdplast och förs in med vinsch eller tryckluft.",
    "Den blåses upp så att den pressas mot rörväggen.",
    "Härdning sker med ånga, varmt vatten eller UV-ljus.",
    "Slangen klipps vid anslutningar och sidogrenar öppnas med robot.",
    "Ny kamera inspektion dokumenterar resultatet."]) +
    sec("Varför metoden dominerar", [
    "Strumpmetoden klarar krökar, ger ett skarvfritt rör och kan användas i de flesta rördimensioner. Den är snabb, kräver ingen schaktning och passar både villa och bostadsrätt."]),
  "faq":[("Vad betyder CIPP?","Cured In Place Pipe, alltså rör som härdas på plats. Det är det internationella namnet på strumpmetoden."),
         ("Kan man använda strumpmetoden på alla rör?","Den fungerar på de flesta rörsystem där rören är hela och har rätt fall. En inspektion avgör.")],
 },
 "relining-av-gjutarror": {
  "h1":"Relining av gjutjärnsrör: så gör man",
  "title":"Relining av gjutjärnsrör – metod, pris och livslängd | Reliningkoll",
  "desc":"Gjutjärnsrör från 1900-talet rostar inifrån. Här är hur relining av gjutjärns- och betongrör går till och vad det kostar.",
  "body": sec("Varför gjutjärnsrör behöver åtgärdas", [
    "Äldre gjutjärnsrör rostar inifrån och bygger upp avlagringar som minskar flödet och till slut ger stopp. Relining ger ett nytt, slätt rör inuti det gamla utan att stammen grävs fram eller rivs."]) +
    sec("Så skiljer sig gjutjärn från andra material", []) + ul([
    "Rören är ofta grövre och tyngre, vilket kräver kraftigare rengöring.",
    "Inre rost och kanter måste slipas ned noggrant för att fodret ska fästa.",
    "Äldre system har ofta grenrör och avvikande dimensioner.",
    "Inspektion är avgörande för om metoden ens är möjlig."]) +
    sec("Pris och livslängd", [
    "Relining av gjutjärnsstammar i en villa ligger vanligen mellan 80 000 och 250 000 kr före ROT-avdrag. Livslängden anges oftast till 40 till 50 år."]),
  "faq":[("Går det att relina gjutjärnsrör med sprickor?","Mindre sprickor går ofta bra. Är röret kollapsat eller saknar fall kan ett byte vara nödvändigt."),
         ("Är relining av gjutjärn ROT-berättigat?","Ja, arbetskostnaden för relining i egen villa är ROT-berättigad.")],
 },
 "relining-av-skorsten": {
  "h1":"Relining av skorsten och rökkanal",
  "title":"Relining av skorsten – infodring av rökkanal (guide) | Reliningkoll",
  "desc":"Relining av skorsten och ventilationskanaler tätar rökkanaler invändigt. Här är hur det går till, när det krävs och vad du betalar.",
  "body": sec("När skorstenen behöver fodras om", [
    "Gamla rökkanaler av tegel eller betong kan vara otäta, spruckna eller felaktigt dimensionerade för dagens pannor och kaminer. Infodring ger en tät, slät kanal inuti den gamla."]) +
    sec("Metoder", []) + ul([
    "Flexibelt rör som förs ned i kanalen och isoleras.",
    "Sprutbetong eller beläggning på kanalens insida.",
    "Prefabricerade insatsrörsblock vid kraftigt skadade kanaler."]) +
    sec("När du bör fodra om", [
    "Om rök tränger ut, om pannan kräver annan dimension eller vid besiktning som påpekar brister. Kontrollera alltid att entreprenören följer gällande branschregler och att sotaren godkänner resultatet."]),
  "faq":[("Krävs tillstånd för att fodra om en skorsten?","Arbetet ska utföras enligt branschregler och sotarens anvisningar. Ofta behövs en besiktning efteråt."),
         ("Kan man relina ventilationskanaler?","Ja, samma princip används för att täta och förnya ventilationskanaler.")],
 },
 "relining-av-ventilation": {
  "h1":"Relining av ventilationskanaler",
  "title":"Relining av ventilation – förnya kanaler utan rivning | Reliningkoll",
  "desc":"Relining av ventilationskanaler förnyar kanaler från insidan utan att schakt eller innertak rivs. Så fungerar det och när det är värt det.",
  "body": sec("Varför fodra ventilationskanaler", [
    "Ventilationskanaler samlar damm, fett och ibland mögel. Otäta kanaler ger sämre inomhusluft och energiförluster. Relining ger en tät, slät kanal inuti den befintliga."])  +
    sec("När det passar", []) + ul([
    "Oåtkomliga kanaler i schakt och bjälklag.",
    "Kanaler med läckage eller korrosion.",
    "Fastigheter där rivning inte är praktiskt möjlig."]) +
    sec("Tänk på", [
    "Relining ersätter inte ventilationsrengöring. Kanalsystemet behöver fortfarande rensas och besiktigas enligt OVK."]),
  "faq":[("Ersätter relining OVK?","Nej. OVK är en obligatorisk ventilationskontroll och gäller oavsett om kanalerna relinas."),
         ("Blir kanalen trängre?","Innerdiametern minskar något, vilket dimensioneringen måste ta hänsyn till.")],
 },
 "stopp-i-avlopp": {
  "h1":"Stopp i avloppet: orsaker och vad som hjälper",
  "title":"Stopp i avloppet – vad gör man? Orsaker och åtgärder | Reliningkoll",
  "desc":"Stopp i avloppet? Här är de vanligaste orsakerna, vad du kan fixa själv och när du bör anlita en spolfirma eller rörinspektör.",
  "body": sec("Vanligaste orsakerna", [
    "Ett stopp kommer sällan av en slump. Oftast handlar det om fett, matrester, hår eller rotinträngning. Är stoppet återkommande är det ett tecken på att rören behöver ses över."]) + ul([
    "Fett och matrester i köksavloppet.",
    "Hår och tvålrester i badrummet.",
    "Främmande föremål som spolats ned.",
    "Rötter som trängt in i utvändiga ledningar.",
    "Rost och avlagringar i äldre gjutjärnsrör.",
    "Felaktigt fall eller sättningar i ledningen."]) +
    sec("Vad du kan göra själv", [
    "Vid ett enkelt stopp hjälper ibland kokhett vatten, en vaskrensare eller avloppsrens. Undvik starka kemikalier som kan skada rören och miljön, särskilt i äldre system."]) +
    sec("När du bör anlita proffs", [
    "Återkommande stopp, stopp som sitter långt in eller misstanke om rotinträngning kräver spolning med högtryck och ofta kamerainspektion. Då ser man orsaken och kan avgöra om relining behövs."]),
  "faq":[("Vad kostar avloppsspolning?","En spolning ligger vanligen mellan 1 500 och 4 500 kr beroende på omfattning och tidpunkt."),
         ("Kommer stoppet tillbaka?","Är orsaken avlagringar eller rötter kommer stoppet ofta tillbaka. Då är inspektion och eventuell relining rätt åtgärd.")],
 },
 "rotavdrag-relining": {
  "h1":"ROT-avdrag på relining: så mycket får du tillbaka",
  "title":"ROT-avdrag på relining 2026 – regler och exempel | Reliningkoll",
  "desc":"Relining i egen villa är ROT-berättigat. Här är reglerna, hur mycket du får tillbaka, taket per person och vad som inte omfattas.",
  "body": sec("Reglerna i korthet", [
    "Du kan dra av 30 procent av arbetskostnaden för relining i din egen villa, med ett tak på 50 000 kr per person och år. Om två äger huset kan ni använda bådas avdrag."]) +
    sec("Räkneexempel", [],) + ul([
    "Total kostnad 120 000 kr, varav 80 000 kr arbete och 40 000 kr material.",
    "ROT-avdrag: 30 procent av 80 000 kr = 24 000 kr.",
    "Du betalar 96 000 kr efter avdrag."]) +
    sec("Detta omfattas inte", [
    "Bostadsrätter och hyresrätter är inte ROT-berättigade. För en bostadsrättsförening hanteras kostnaden i stället via föreningens underhåll."]),
  "faq":[("Måste man vara folkbokförd i huset?","Du ska äga och bo i bostaden för att använda ROT-avdraget."),
         ("Kan man använda ROT-avdraget flera år i rad?","Taket gäller per person och år, och du kan använda det varje år så länge du har arbetskostnader.")],
 },
}

def build_guides():
    cards = ''.join(
      f'<a class="card rv" href="/guider/{slug}/"><h2>{esc(g["h1"].split(":")[0].split("?")[0])}</h2><p>{esc(g["desc"][:110])}…</p></a>'
      for slug,g in GUIDES.items())
    body = f'''<section class="hero"><div class="wrap narrow">
      {crumb_html([("Hem","/"),("Guider","/guider/")])}
      <h1 class="h1">Guider om relining och avlopp</h1>
      <p class="lead">Allt du behöver veta innan du beställer: metoder, priser, livslängd och fallgropar.</p>
    </div></section>
    <section><div class="wrap"><div class="grid grid-3">{cards}</div></div></section>
    <section><div class="wrap"><div class="cta-band rv"><h2>Redo att jämföra?</h2>
      <p>Få upp till tre offerter från lokala reliningfirmor. Gratis och utan förpliktelse.</p>
      <a class="btn btn-primary btn-lg" href="/offert/">Få offerter</a></div></div></section>'''
    write("/guider/index.html", page("Guider om relining och avlopp – metoder, priser och råd",
      "Guider om relining och avlopp: metoder, priser, livslängd, gjutjärnsrör, skorsten och ROT-avdrag. Allt förklarat enkelt och utan krångel.",
      "/guider/", body, crumb=[("Hem","/"),("Guider","/guider/")]))

    guide_slugs = list(GUIDES)
    for slug, g in GUIDES.items():
        faq = g.get("faq", [])
        _i = guide_slugs.index(slug)
        others = [guide_slugs[(_i + k) % len(guide_slugs)] for k in range(1, 5)]
        _sum = SUMMARY.get(slug)
        sum_box = (f'<div class="answer"><p><strong>Kort svar.</strong> {esc(_sum)}</p></div>'
                   if _sum else '')
        _chk = CHECK.get(slug)
        check_block = ('<h2>Checklista</h2><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in _chk) + '</ul>'
                       ) if _chk else '' 
        rel = ('<h2>Relaterade guider</h2><div class="pills">'
               + ''.join(f'<a href="/guider/{x}/">{esc(GUIDES[x]["h1"].split(":")[0].split("?")[0])}</a>' for x in others)
               + '<a href="/pris/">Priser 2026</a><a href="/relining/">Hitta firmor i din kommun</a>'
               + '<a href="/guider/">Alla guider</a></div>')
        body = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Guider","/guider/"),(g["h1"],f"/guider/{slug}/")])}
          <h1 class="h1">{esc(g["h1"])}</h1>
          <p class="lead">{esc(g["desc"])}</p>
          <p class="meta-line">Uppdaterad 2026 &middot; Läs tid ca 6 min</p>
          {sum_box}
        </div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          {g["body"]}
          {g.get("body2","")}
          {check_block}
          <h2>Vanliga frågor</h2>
          <div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in faq)}</div>
          {rel}
          <div class="cta-band" style="margin-top:40px"><h2>{esc(g["h1"].split(":")[0].split("?")[0])} för ditt projekt?</h2>
            <p>Beskriv ditt ärende och få upp till tre offerter från lokala firmor. Gratis.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Få offerter</a></div>
        </div></div></section>'''
        write(f"/guider/{slug}/index.html", page(g["title"], g["desc"], f"/guider/{slug}/", body,
              faq=faq, crumb=[("Hem","/"),("Guider","/guider/"),(g["h1"],f"/guider/{slug}/")]))

if __name__ == "__main__":
    C.build_home()
    build_guides()
    print("del 1 klar")
