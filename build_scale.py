#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skalar reliningkoll.se till 400+ sidor:
 - 16 nya djupguider
 - 9 nya prissidor
 - 30 firmaprofiler
 - avloppsspolning + rörinspektion per kommun (stora orter)
"""
import sys, os, json
sys.path.insert(0, "/home/clawd/reliningkoll")
import build_core as C
from build_core import page, crumb_html, write, esc, logo_ph, BASE, FORM_EMAIL
from build_part1 import sec, ul
import build_muni as M

TODAY = "2026-11-06"

# ================================================================ NYA GUIDER
NEW_GUIDES = {
"hur-lang-tid-tar-relining": {
 "h1":"Hur lång tid tar en relining?",
 "title":"Hur lång tid tar relining? Tidsplan för villa och BRF | Reliningkoll",
 "desc":"En relining tar oftast tre till fem arbetsdagar i en villa. Här är hela tidsplanen, vad som påverkar och varför stambyte tar veckor.",
 "body": sec("Kort svar: tre till fem arbetsdagar",[
   "En normal relining av ett villaavlopp tar tre till fem arbetsdagar. En stam i en lägenhet går snabbare, medan ett helt flerfamiljshus delas upp i etapper som kan pågå i flera veckor. Själva härdningen av fodret tar bara några timmar per rör – det är förberedelse, rengöring och återställande av anslutningar som tar tid."]) +
   sec("Tidsplan steg för steg",[])+ul([
   "Dag 1: rörinspektion, högtrycksspolning och nedslipning av rörens insida.",
   "Dag 2: fodret mättas, förs in och härdas. Anslutningar öppnas upp.",
   "Dag 3: golvbrunnar och grenrör tätas, ny kamera inspektion dokumenterar resultatet.",
   "Dag 4–5: efterarbete, kontroll och eventuell återställning av ytskikt."]) +
   sec("Vad påverkar tiden?",[
   "Rörens längd och antal grenrör, hur svårtillgängliga de är och om arbetet sker i etapper för att de boende ska kunna använda avloppet. I en BRF planeras ofta en stam per dag så att lägenheterna bara berörs kort."]) +
   sec("Kan jag bo kvar?",[
   "Ja, i villa och bostadsrätt kan du normalt bo kvar. Vattnet kan vara avstängt några timmar under härdningen, och du får reda på i förväg vilka dagar."]),
 "faq":[("Tar relining längre tid än stambyte?","Nej, tvärtom. Stambyte tar ofta veckor till månader och kräver rivning, medan relining klarar samma stam på tre till fem dagar."),
        ("Kan arbetet delas upp?","Ja, särskilt i flerfamiljshus planeras arbetet stambyggt etappvis så att boende bara berörs kort.")]},

"relining-garanti": {
 "h1":"Garanti på relining – vad du bör kräva",
 "title":"Garanti på relining – så länge gäller den | Reliningkoll",
 "desc":"Branschen lämnar normalt tio års garanti på relining, ibland längre. Här är vad garantin ska omfatta och hur du kontrollerar den.",
 "body": sec("Vad garantin omfattar",[
   "En seriös entreprenör lämnar skriftlig garanti på utförandet. Vanligast är tio år, men vissa system och leverantörer ger längre. Garantin ska täcka att fodret sitter fast, är tätt och att anslutningar och golvbrunnar håller."]) +
   sec("Kräv alltid dokumentationen",[])+ul([
   "Kamera inspektion före arbetet som visar utgångsläget.",
   "Kamera inspektion efter arbetet som visar resultatet.",
   "Protokoll över vilket foder och vilken härdmetod som använts.",
   "Skriftlig garanti med tydlig ansvarstid och kontaktväg."]) +
   sec("Skillnad på garanti och försäkring",[
   "Garantin är entreprenörens löfte om utförandet. Försäkringen täcker skador som uppstår. Båda behövs, och du bör kontrollera att entreprenören har giltig ansvarsförsäkring innan arbetet börjar."]),
 "faq":[("Hur lång garanti är rimlig?","Tio år på utförandet är branschstandard. Längre garanti är ett plus men ersätter inte korrekt dokumentation."),
        ("Vad gör jag om fodret lossnar?","Reklamera skriftligt till entreprenören och hänvisa till garantin. Spara inspektionsfilmerna som bevis.")]},

"tecken-pa-att-ror-behover-byta": {
 "h1":"Tecken på att avloppsrören behöver åtgärdas",
 "title":"Tecken på dåliga avloppsrör – 8 varningssignaler | Reliningkoll",
 "desc":"Återkommande stopp, missfärgat vatten och dålig lukt kan betyda att rören är slitna. Här är tecknen du ska ta på allvar.",
 "body": sec("Åtta varningssignaler",[
   "Avloppsrör ger sällan upp utan förvarning. Oftast kommer flera små tecken innan ett allvarligt problem uppstår. Känner du igen flera av punkterna nedan bör du beställa en rörinspektion."])+ul([
   "Återkommande stopp trots spolning.",
   "Vatten som rinner undan långsamt i flera avlopp samtidigt.",
   "Missfärgat eller illaluktande vatten i vaskar och dusch.",
   "Gurglande ljud från avloppet när något spolas.",
   "Dålig lukt som inte försvinner trots rengöring.",
   "Fukt eller missfärgning på golv intill golvbrunnar.",
   "Rostfärgade ränder i avloppet (tyder på gjutjärn som rostat).",
   "Träd eller buskar vars rötter växer nära avloppsledningen."]) +
   sec("Vad du gör härnäst",[
   "Boka en kamera inspektion. Den visar rörens skick, om det finns rötter, sprickor eller avlagringar, och ger ett underlag för att avgöra om relining, spolning eller ett rörbyte är rätt åtgärd."]),
 "faq":[("Räcker det att spola?","Vid avlagringar hjälper spolning tillfälligt. Återkommer stoppet tyder det på att rören behöver relinas eller bytas."),
        ("Hur ofta bör man inspektera?","I hus med gjutjärnsrör: vart femte till tionde år, eller så snart du ser något av tecknen ovan.")]},

"stambyte-kostnad": {
 "h1":"Vad kostar ett stambyte? Priser och alternativ",
 "title":"Stambyte kostnad 2026 – pris för villa och BRF | Reliningkoll",
 "desc":"Stambyte kostar ofta 25 till 50 procent mer än relining. Här är priser för villa och flerfamiljshus och när relining är ett billigare alternativ.",
 "body": sec("Riktpriser 2026",[])+ul([
   "Villa, komplett stambyte: 150 000 – 400 000 kr.",
   "Lägenhet, per stam: 80 000 – 160 000 kr.",
   "Flerfamiljshus, hela fastigheten: 2 – 6 miljoner kr.",
   "Återställning av badrum och kök tillkommer ofta."]) +
   sec("Varför stambyte blir dyrare än det ser ut",[
   "Dör ett stambyte räknar många bara rörkostnaden. I praktiken tillkommer rivning av golv och väggar, nytt kakel i badrum, nytt kök, el och VVS, samt evakuering av boende under arbetet. Det är därför relining, som gör samma stam tät utan rivning, ofta blir betydligt billigare."]) +
   sec("När stambyte ändå krävs",[
   "Är rören kollapsade, har fel dimension eller rör sig byggnaden kraftigt kan relining vara omöjligt. En rörinspektion avgör vilket som gäller för din fastighet."]),
 "faq":[("Är relining eller stambyte billigast?","Relining är normalt 25 till 50 procent billigare eftersom ingen rivning behövs."),
        ("Måste man flytta ut vid stambyte?","Ja, oftast evakueras bostaden under delar av arbetet. Vid relining kan du bo kvar.")]},

"relining-av-betongror": {
 "h1":"Relining av betongrör",
 "title":"Relining av betongrör – metod och pris | Reliningkoll",
 "desc":"Betongrör spricker och nöts med tiden. Här är hur relining av betongrör går till, när det passar och vad det kostar.",
 "body": sec("Varför betongrör behöver åtgärdas",[
   "Betongrör används ofta i äldre källare och utvändiga ledningar. Med tiden uppstår sprickor, fogar vittrar och avlagringar byggs upp. Relining ger ett nytt, slätt rör inuti det gamla."])+ul([
   "Sprickor och vittrade fogar tätas invändigt.",
   "Röret blir slätt och får bättre flöde.",
   "Ingen schaktning krävs för ledningar i mark.",
   "Kräver att röret är helt och har rätt fall."]) +
   sec("Pris",[
   "Relining av betongrör ligger vanligen mellan 800 och 1 500 kr per meter, beroende på dimension och åtkomst. Utvändiga ledningar som grävs fram kan bli dyrare."]),
 "faq":[("Kan man relina spruckna betongrör?","Mindre sprickor går bra. Är röret kollapsat eller har tappat fall kan ett byte vara nödvändigt."),
        ("Fungerar relining i mark?","Ja, men åtkomst till ledningen påverkar priset. En inspektion avgör förutsättningarna.")]},

"relining-av-plastror": {
 "h1":"Relining av plaströr (PVC)",
 "title":"Relining av plaströr – när det behövs och pris | Reliningkoll",
 "desc":"Plaströr från 1970-talet kan bli spröda och spricka. Här är när relining av PVC-rör är rätt lösning och vad den kostar.",
 "body": sec("När plaströr behöver relinas",[
   "Äldre PVC- och PP-rör blir med tiden spröda, särskilt vid värme och kemikalier. Fogmuffar kan läcka och rören spricka vid sättningar. Relining förnyar insidan och ger ett tätt system."])+ul([
   "Läckande fogmuffar och sprickor.",
   "Rör som blivit spröda och missfärgade.",
   "Återkommande stopp i äldre plastledningar.",
   "Kräver inspektion för att utesluta kollaps."]) +
   sec("Pris och livslängd",[
   "Relining av plaströr ligger i samma intervall som gjutjärn, vanligen 800 till 1 500 kr per meter. Livslängden anges normalt till 40 till 50 år."]),
 "faq":[("Är det värt att relina plaströr?","Ja, om rören är slitna men hela. Det ger ett tätt system utan rivning och förlänger livslängden avsevärt."),
        ("Hur vet jag om plaströren är dåliga?","En kamera inspektion visar sprickor, sprödhet och fogstatus.")]},

"avloppsspolning-eller-relining": {
 "h1":"Avloppsspolning eller relining – vad behöver du?",
 "title":"Spolning eller relining? Så väljer du rätt åtgärd | Reliningkoll",
 "desc":"Spolning löser akuta stopp, relining förnyar rören. Här är skillnaden och hur du avgör vilken åtgärd ditt avlopp behöver.",
 "body": sec("Den enkla skillnaden",[
   "Spolning tar bort det som täpper igen röret här och nu. Relining förnyar själva röret inifrån och löser orsaken. Ett enstaka stopp klarar sig oftast med spolning – återkommande problem betyder att rören behöver ses över."]) +
   '<table class="tbl"><thead><tr><th>Problem</th><th>Åtgärd</th></tr></thead><tbody>' +
   '<tr><td>Enstaka stopp</td><td>Avloppsspolning</td></tr>' +
   '<tr><td>Återkommande stopp</td><td>Rörinspektion, ofta relining</td></tr>' +
   '<tr><td>Dålig lukt och missfärgat vatten</td><td>Rörinspektion</td></tr>' +
   '<tr><td>Rötter i ledningen</td><td>Spolning + relining</td></tr>' +
   '<tr><td>Rost och avlagringar i gjutjärn</td><td>Relining</td></tr></tbody></table>' +
   sec("Varför inspektion först",[
   "En kamera inspektion visar om rören är hela. Är de det räcker spolning och skötsel. Är de slitna är det billigare att relina nu än att spola om och om igen."]),
 "faq":[("Kan man relina efter spolning?","Ja. Spolning och rengöring är alltid första steget även inför en relining."),
        ("Hur ofta kommer stoppet tillbaka om man bara spolar?","Vid avlagringar eller rötter kan stoppet återkomma inom några månader. Då är inspektion rätt nästa steg.")]},

"stopp-i-dusch-och-badkar": {
 "h1":"Stopp i duschen eller badkaret – så löser du det",
 "title":"Stopp i dusch och badkar – orsaker och åtgärder | Reliningkoll",
 "desc":"Stopp i duschen beror oftast på hår och tvålrester. Här är vad du kan fixa själv och när du bör kalla på en spolfirma.",
 "body": sec("Vanligaste orsaken",[
   "I dusch och badkar är det nästan alltid hår som blandas med tvålrester och bildar en propp i vattenlåset eller röret. Detta skiljer sig från köksavloppet, där fett dominerar."]) +
   sec("Vad du kan göra själv",[])+ul([
   "Ta bort synligt hår från golvbrunnen.",
   "Skruva loss och rengör vattenlåset.",
   "Använd en vaskrensare eller rensvajer.",
   "Spola med kokhett vatten i omgångar."]) +
   sec("När du bör anlita proffs",[
   "Sitter stoppet längre in eller återkommer det snabbt behövs högtrycksspolning. Är rören gamla och gjutjärn kan stoppet bero på invändig rost – då ger en rörinspektion svaret."]),
 "faq":[("Hjälper avloppsrens?","Enzymbaserat rens kan hjälpa mot tvålrester, men undvik starka kemikalier som kan skada äldre rör."),
        ("Kommer stoppet tillbaka?","Om rören är belagda invändigt återkommer stoppet. Då är inspektion och eventuell relining rätt åtgärd.")]},

"stopp-i-tvattmaskin": {
 "h1":"Stopp i tvättmaskinen och avloppet",
 "title":"Stopp i tvättmaskin – orsaker och vad du gör | Reliningkoll",
 "desc":"Tvättmaskinen töms dåligt eller vattnet stiger i avloppet? Här är orsakerna och vad du kan göra själv före du ringer proffs.",
 "body": sec("Vanliga orsaker",[
   "Tvättmaskiner ger ifrån sig ludder och fiber som kan bygga upp proppar i avloppsröret. Äldre gjutjärnsrör med invändig rost gör problemet värre."])+ul([
   "Ludder och fiber i vattenlås eller rör.",
   "Röret från maskinen har fel fall eller är för långt.",
   "Invändig rost i äldre gjutjärnsrör.",
   "Återkommande läckage vid kopplingen."]) +
   sec("Vad du gör",[
   "Kontrollera vattenlåset och rengör det. Leder problemet vidare in i röret behövs spolning. Vid återkommande stopp i tvättstugan är rörinspektion nästa steg."]),
 "faq":[("Kan jag spola själv?","Enkla proppar i vattenlåset går att rensa själv. Röret längre in kräver högtrycksspolning."),
        ("Hjälper relining?","Om orsaken är invändig rost eller avlagringar i röret är relining en hållbar lösning.")]},

"avlopp-luktar-illa": {
 "h1":"Avloppet luktar illa – orsaker och åtgärder",
 "title":"Avlopp luktar illa? Orsaker och vad som hjälper | Reliningkoll",
 "desc":"Dålig lukt från avloppet betyder oftast att vattenlåset inte håller tätt eller att rören är belagda. Här är orsakerna och lösningarna.",
 "body": sec("Vanliga orsaker",[
   "Lukt betyder att avloppsgas tar sig upp. Det kan bero på ett uttorkat vattenlås, en läckande fog eller beläggningar i rören som bildar bakterier."])+ul([
   "Vattenlås som torkat ut i sällan använda avlopp.",
   "Läckande fogar eller otäta anslutningar.",
   "Beläggningar och biofilm i rören.",
   "Felinstallation av vattenlås eller backventil.",
   "Övergolv eller golvbrunn som saknar vattenlås."]) +
   sec("Vad du gör",[
   "Spola igenom sällan använda avlopp så att vattenlåset fylls. Luktar det ändå kan det finnas beläggningar i rören som kräver spolning och inspektion. Vid gamla rör kan lukten vara ett tecken på att insidan är sliten, vilket relining åtgärdar."]),
 "faq":[("Är dålig lukt farlig?","Avloppsgas kan vara skadlig i höga koncentrationer. Får du bestående lukt bör du låta en fackman inspektera rören."),
        ("Löser relining lukt?","Ja, om lukten kommer från slitna rör med beläggningar. Relining ger en slät, tät insida utan biofilm.")]},

"backventil-och-vattenlas": {
 "h1":"Backventil och vattenlås i avloppet",
 "title":"Backventil avlopp – så fungerar den och när den behövs | Reliningkoll",
 "desc":"Backventil hindrar avloppsvatten från att tränga upp i källare och låga rum. Här är hur den fungerar och när du behöver en.",
 "body": sec("Vad en backventil gör",[
   "En backventil släpper igenom vatten ut men stänger om flödet vänder. Den används i källare, källarbrunnar och golvbrunnar i låga rum för att förhindra översvämning vid stopp i det kommunala nätet."])+ul([
   "Krävs i rum under avloppets uppstigningsnivå.",
   "Ska kombineras med vattenlås.",
   "Kräver regelbunden rengöring för att fungera.",
   "Kan behöva bytas när packningen blir sliten."]) +
   sec("Vattenlåsets roll",[
   "Vattenlåset stänger ute avloppsgas med en vattenpropp. Torkar det ut kommer lukt in. Kontrollera därför att alla golvbrunnar och avlopp har fungerande vattenlås."]),
 "faq":[("Behöver jag backventil?","Har du källare eller rum under gatunivå och risk för uppdämning i det kommunala nätet är en backventil en billig försäkring."),
        ("Kan backventil stoppa lukt?","Nej, lukt stängs främst ute av vattenlåset. Backventilen hindrar vatten från att tränga upp.")]},

"valja-reliningfirma": {
 "h1":"Så väljer du rätt reliningfirma",
 "title":"Välja reliningfirma – 10 saker att kontrollera | Reliningkoll",
 "desc":"Rätt reliningfirma avgör resultatet i 40 år. Här är tio saker att kontrollera innan du skriver avtal.",
 "body": sec("Checklista innan du beställer",[
   "Relining är en långsiktig investering. Skillnaden mellan en seriös och en mindre noggrann entreprenör märks inte på priset utan på dokumentationen."])+ul([
   "Godkänd F-skatt och momsregistrering.",
   "Giltig ansvarsförsäkring.",
   "Inga betalningsanmärkningar hos Kronofogden.",
   "Erfarenhet av just din rörtyp och dimension.",
   "Referensobjekt du kan kontakta.",
   "Skriftlig garanti, normalt tio år eller mer.",
   "Kamera inspektion före och efter arbetet.",
   "Tydlig beskrivning av vilket foder och vilken metod.",
   "Fast pris eller tydlig prisspecifikation.",
   "Färdig dokumentation efter avslutat arbete."]) +
   sec("Jämför minst tre offerter",[
   "Skiljer sig offerterna kraftigt i pris, granska vad som ingår. En låg offert saknar ofta inspektion, dokumentation eller garanti. Jämför alltid på lika villkor, inte på lägsta pris."]),
 "faq":[("Är billigast bäst?","Nej. Fodrets kvalitet, hantverkarens rutin och dokumentationen väger tyngre än några tusenlappar."),
        ("Vad kräver jag i offerten?","Inspektion före och efter, angiven metod och garanti samt allt som ingår skriftligt.")]},

"fragor-till-reliningfirma": {
 "h1":"10 frågor att ställa till din reliningfirma",
 "title":"Frågor att ställa till en reliningfirma | Reliningkoll",
 "desc":"Ställ rätt frågor innan du beställer relining. Här är tio frågor som skiljer en seriös entreprenör från en mindre noggrann.",
 "body": sec("Frågorna som avgör",[
   "En erfaren entreprenör svarar enkelt på alla dessa. Undvikligare svar är en varningssignal."])+ul([
   "Vilken metod och vilket foder använder ni?",
   "Har ni gjort en kamera inspektion innan offerten?",
   "Hur påverkas rörets innerdiameter?",
   "Vad ingår i priset, och vad är tillval?",
   "Hur lång garanti lämnar ni, och på vad?",
   "Får jag inspektionsfilm före och efter?",
   "Har ni referensobjekt jag kan kontakta?",
   "Hur hanteras anslutningar och golvbrunnar?",
   "Vem utför arbetet – egen personal eller underentreprenör?",
   "Hur lång tid tar arbetet i min fastighet?"]) +
   sec("Så tolkar du svaren",[
   "Klara, specifika svar tyder på rutin. Undvikande svar om garanti, dokumentation eller metod är en varningssignal. Be att få svaren skriftligt i offerten."]),
 "faq":[("Måste jag begära inspektion?","Ja, en seriös offert bygger alltid på en kamera inspektion. Utan den är priset en gissning."),
        ("Kan jag kräva att få filmen?","Ja, du bör få både före- och efterfilmen samt protokollet som dokumentation.")]},

"relining-flerbostadshus": {
 "h1":"Relining i flerbostadshus och fastighetsbolag",
 "title":"Relining flerbostadshus – process för fastighetsägare | Reliningkoll",
 "desc":"Relining i flerbostadshus kräver planering i etapper. Här är processen för fastighetsägare och bostadsrättsföreningar.",
 "body": sec("Varför relining passar flerbostadshus",[
   "I flerbostadshus är ett stambyte dyrt och stör boende i månader. Relining kan utföras stam för stam så att hela huset aldrig står utan avlopp samtidigt. Det sänker både kostnad och störning."]) +
   sec("Process i fem steg",[])+ul([
   "Rörinspektion av samtliga stammar för att kartlägga skick.",
   "Offert och tidsplan uppdelad per stam och trapphus.",
   "Information till boende i god tid inför varje etapp.",
   "Utförande stam för stam, några dagar per stam.",
   "Slutdokumentation och garanti till fastighetsägaren."]) +
   sec("Ekonomi",[
   "Kostnaden ligger normalt mellan 50 000 och 120 000 kr per stam, med rabatt vid stora projekt. Jämfört med stambyte, som ofta kräver evakuering och återställning av badrum, blir totalkostnaden betydligt lägre."]),
 "faq":[("Kan boende använda avloppet under arbetet?","Ja, normalt berörs en stam i taget och de boende informeras i förväg."),
        ("Får föreningen garanti?","Ja, garantin skrivs på föreningen som beställare och täcker hela anläggningen.")]},

"rotavdrag-avlopp-regler": {
 "h1":"ROT-avdrag för avlopp och relining – reglerna 2026",
 "title":"ROT-avdrag avlopp 2026 – regler och exempel | Reliningkoll",
 "desc":"Relining och rörarbete i egen villa är ROT-berättigat. Här är reglerna, taket och hur du räknar ut avdraget 2026.",
 "body": sec("Reglerna i korthet",[
   "Du får dra av 30 procent av arbetskostnaden för relining och rörarbete i din egen villa, upp till 50 000 kr per person och år. Äger ni huset tillsammans kan båda använda sitt avdrag, vilket ger upp till 100 000 kr per år."]) +
   sec("Räkneexempel",[])+ul([
   "Total kostnad 150 000 kr: 100 000 kr arbete, 50 000 kr material.",
   "ROT-avdrag: 30 procent av 100 000 kr = 30 000 kr.",
   "Du betalar 120 000 kr efter avdrag."]) +
   sec("Detta omfattas inte",[
   "Bostadsrätter och hyresrätter är inte ROT-berättigade. För en bostadsrättsförening hanteras kostnaden i stället via föreningens underhållsplan."]),
 "faq":[("Gäller ROT-avdraget avloppsspolning?","Ja, arbetskostnaden för rörarbete i egen villa är ROT-berättigad."),
        ("Kan jag använda avdraget varje år?","Taket gäller per person och år, och du kan använda det varje år du har arbetskostnader.")]},

"avloppsrenovering-guide": {
 "h1":"Avloppsrenovering – så lägger du upp projektet",
 "title":"Avloppsrenovering – guide från inspektion till garanti | Reliningkoll",
 "desc":"Avloppsrenovering i villa, bostadsrätt eller fastighet. Här är hela processen från inspektion och offert till utförande och garanti.",
 "body": sec("Steg för steg",[
   "En lyckad avloppsrenovering handlar mindre om att välja billigaste firma och mer om att göra rätt saker i rätt ordning. Börja alltid med att ta reda på rörens skick."])+ul([
   "1. Rörinspektion med kamera som visar rörens skick och eventuella problem.",
   "2. Beslut om åtgärd: spolning, relining eller byte.",
   "3. Offert från minst tre entreprenörer på lika villkor.",
   "4. Kontroll av F-skatt, försäkring och referenser.",
   "5. Utförande med dokumentation före och efter.",
   "6. Skriftlig garanti och slutprotokoll."]) +
   sec("Vanliga misstag",[
   "Att beställa utan inspektion, att jämföra offerter som inte omfattar samma saker, och att välja lägsta pris utan att kontrollera garanti och dokumentation. Undvik dessa tre och risken för problem minskar kraftigt."]),
 "faq":[("Vad kostar en avloppsrenovering?","Från några tusenlappar för spolning till 80 000 – 250 000 kr för en komplett villarenovering med relining."),
        ("Hur lång tid tar det?","En relining tar tre till fem dagar. Ett stambyte kan ta veckor till månader.")]},

"relining-vs-rorbyte": {
 "h1":"Relining eller rörbyte – skillnaden förklaras",
 "title":"Relining eller rörbyte? Skillnad, pris och val | Reliningkoll",
 "desc":"Relining förnyar röret inifrån, rörbyte ersätter det. Här är skillnaderna i pris, tid, livslängd och när respektive metod passar.",
 "body": sec("Grundskillnaden",[
   "Rörbyte innebär att de gamla rören tas bort och ersätts med nya. Relining bygger ett nytt rör inuti det gamla. Båda ger ett tätt, modernt system – men de skiljer sig i ingrepp, tid och kostnad."]) +
   '<table class="tbl"><thead><tr><th>Aspekt</th><th>Relining</th><th>Rörbyte</th></tr></thead><tbody>' +
   '<tr><td>Rivning</td><td>Ingen</td><td>Golv, väggar, schakt</td></tr>' +
   '<tr><td>Tid</td><td>3–5 dagar</td><td>Veckor–månader</td></tr>' +
   '<tr><td>Kostnad villa</td><td>80 000 – 250 000 kr</td><td>150 000 – 400 000 kr</td></tr>' +
   '<tr><td>Bo kvar</td><td>Ja</td><td>Nej, evakuering</td></tr>' +
   '<tr><td>Livslängd</td><td>40–50 år</td><td>50 år+</td></tr></tbody></table>' +
   sec("När respektive metod passar",[
   "Relining passar när rören är slitna men hela. Rörbyte krävs när rören kollapsat, har fel dimension eller byggnaden sätter sig kraftigt. En rörinspektion avgör."]),
 "faq":[("Blir relining lika bra som ett rörbyte?","För rör som är hela men slitna ger relining samma funktion till lägre kostnad och utan rivning."),
        ("Kan man byta rör senare ändå?","Ja, men då måste det gamla systemet tas bort. Relining är en långsiktig lösning, inte en tillfällig lapp.")]},
}

# ================================================================ NYA PRISER
NEW_PRICES = {
 "stambyte": {"h1":"Vad kostar ett stambyte?","title":"Stambyte pris 2026 – kostnad villa och BRF | Reliningkoll",
   "desc":"Vad kostar ett stambyte 2026? Priser för villa, lägenhet och flerfamiljshus, samt varför relining ofta blir billigare.",
   "rows":[("Villa, komplett","150 000 – 400 000 kr"),("Lägenhet per stam","80 000 – 160 000 kr"),
     ("Flerfamiljshus, hel fastighet","2 – 6 miljoner kr"),("Återställning badrum/kök","tillkommer ofta")],
   "sections":[("Varför stambyte blir dyrare",["Till rörkostnaden kommer rivning, nytt kakel, kök, el och VVS samt evakuering av boende. Det gör totalkostnaden betydligt högre än relining."]),
     ("Relining som alternativ",["Relining förnyar samma stam utan rivning och är normalt 25 till 50 procent billigare."])],
   "faq":[("Måste man flytta ut?","Ja, oftast evakueras bostaden under delar av ett stambyte."),
     ("Är relining alltid möjligt?","Nej, kollapsade rör eller fel dimension kräver ett byte. Inspektion avgör.")]},
 "relining-flerbostadshus": {"h1":"Relining pris flerbostadshus","title":"Relining flerbostadshus pris 2026 | Reliningkoll",
   "desc":"Pris för relining i flerbostadshus och fastighetsbolag. Kostnad per stam och för hela fastigheten.",
   "rows":[("Per stam","50 000 – 120 000 kr"),("Per lägenhet","40 000 – 80 000 kr"),
     ("Hela fastigheten, 20 lgh","1,5 – 3 miljoner kr")],
   "sections":[("Rabatt vid stora projekt",["Ju fler stammar som relinas i samma projekt, desto lägre pris per stam eftersom etablering och inspektion delas."])],
   "faq":[("Kan arbetet delas upp?","Ja, stam för stam så att boende bara berörs kort.")]},
 "avloppsrensning": {"h1":"Avloppsrensning och spolning – pris","title":"Avloppsrensning pris 2026 – kostnad spolning | Reliningkoll",
   "desc":"Vad kostar avloppsrensning och högtrycksspolning 2026? Priser för villa och fastighet samt akut utryckning.",
   "rows":[("Rensning enkel propp","800 – 1 800 kr"),("Högtrycksspolning villa","1 500 – 3 500 kr"),
     ("Spolning fastighet","3 000 – 6 000 kr"),("Akut kväll/helg","2 000 – 5 000 kr")],
   "sections":[("När räcker rensning?",["Ett enstaka stopp kan ofta lösas med rensning. Återkommer problemet krävs spolning och inspektion."])],
   "faq":[("Kan jag undvika återkommande stopp?","Om orsaken är avlagringar eller rötter i röret hjälper bara spolning och eventuell relining.")]},
 "relining-per-meter": {"h1":"Pris per meter för relining","title":"Relining pris löpmeter 2026 | Reliningkoll",
   "desc":"Kostnad per meter för relining 2026, för avloppsrör, stam och gjutjärn. Så räknar du ut ditt pris.",
   "rows":[("Avloppsrör villa","800 – 1 200 kr/m"),("Stam flerbostadshus","1 000 – 1 500 kr/m"),
     ("Gjutjärn rostigt","1 100 – 1 500 kr/m")],
   "sections":[("Varför meterpriset varierar",["Krökar, dimension och rörens skick påverkar tiden per meter. Raka rör går snabbare än stammar med många grenrör."])],
   "faq":[("Räknas anslutningar per meter?","Nej, anslutningar och golvbrunnar debiteras oftast styckvis utöver meterpriset.")]},
 "rorinspektion-kamera": {"h1":"Pris rörinspektion med kamera","title":"Rörinspektion pris 2026 – kostnad kamerainspektion | Reliningkoll",
   "desc":"Vad kostar en rörinspektion med kamera 2026? Priser för villa och fastighet samt vad rapporten innehåller.",
   "rows":[("Inspektion villa","0 – 2 500 kr"),("Inspektion fastighet","5 000 – 40 000 kr"),
     ("I samband med relining","Ofta inkluderad")],
   "sections":[("Varför inspektion är avgörande",["Utan inspektion går det inte att veta rörens skick eller dimension. Alla seriösa offerter bygger på en inspektion."])],
   "faq":[("Får jag behålla filmen?","Ja, du bör få film och protokoll dokumenterat.")]},
 "rotavdrag": {"h1":"ROT-avdrag – vad du får tillbaka","title":"ROT-avdrag 2026 – regler, tak och exempel | Reliningkoll",
   "desc":"ROT-avdrag 2026: 30 procent av arbetskostnaden, tak 50 000 kr per person och år. Här är reglerna och räkneexempel.",
   "rows":[("Avdrag","30 % av arbetskostnaden"),("Tak","50 000 kr per person/år"),
     ("Två ägare","Upp till 100 000 kr/år")],
   "sections":[("Vad som är ROT-berättigat",["Arbetskostnaden för relining och rörarbete i egen villa. Material räknas inte."]),
     ("Detta omfattas inte",["Bostadsrätt och hyresrätt är inte ROT-berättigade."])],
   "faq":[("Gäller det avloppsspolning?","Ja, arbetskostnaden för rörarbete i egen villa är ROT-berättigad.")]},
 "avloppsrenovering": {"h1":"Kostnad avloppsrenovering","title":"Avloppsrenovering pris 2026 – kostnad komplett | Reliningkoll",
   "desc":"Vad kostar en avloppsrenovering 2026? Priser från spolning till komplett renovering med relining.",
   "rows":[("Spolning","1 500 – 4 500 kr"),("Inspektion","0 – 2 500 kr"),
     ("Relining villa","80 000 – 250 000 kr"),("Stambyte villa","150 000 – 400 000 kr")],
   "sections":[("Så håller du nere kostnaden",["Beställ inspektion först, jämför tre offerter på lika villkor och utnyttja ROT-avdraget i villa."])],
   "faq":[("Vad är billigast?","Spolning för akuta stopp, relining för slitna men hela rör – klart billigare än stambyte.")]},
 "gjutarror": {"h1":"Pris relining av gjutjärnsrör","title":"Relining gjutjärnsrör pris 2026 | Reliningkoll",
   "desc":"Kostnad för relining av gjutjärnsrör 2026. Priser för villa och fastighet samt vad som påverkar.",
   "rows":[("Gjutjärn villa","90 000 – 260 000 kr"),("Per meter","1 100 – 1 500 kr/m"),
     ("Fastighet per stam","60 000 – 130 000 kr")],
   "sections":[("Varför gjutjärn kräver mer",["Invändig rost och kanter måste slipas ned noggrant för att fodret ska fästa, vilket tar längre tid än på slätare rör."])],
   "faq":[("Är gjutjärn svårare att relina?","Något, eftersom rengöringen är mer krävande. Men det är en av de vanligaste situationerna.")]},
 "stopp-i-avlopp": {"h1":"Pris för att åtgärda stopp i avlopp","title":"Stopp i avlopp pris 2026 – kostnad åtgärd | Reliningkoll",
   "desc":"Vad kostar det att åtgärda stopp i avloppet 2026? Priser för rensning, spolning och akut utryckning.",
   "rows":[("Rensning","800 – 1 800 kr"),("Spolning villa","1 500 – 3 500 kr"),
     ("Akut kväll/helg","2 000 – 5 000 kr")],
   "sections":[("Så undviker du återkommande stopp",["Förebyggande spolning vartannat till var femte år och att inte spola ned fett eller hår minskar risken markant."])],
   "faq":[("Kan stoppet bli dyrare?","Vid rötter eller fel på ledningen i mark kan kostnaden stiga. Inspektion ger svar.")]},
}

# ================================================================ NYA FIRMOR
# (slug, namn, ort, län, metoder, sedan)
NEW_FIRMS = [
 ("stockholms-stamteknik","Stockholms Stamteknik AB","Stockholm","Stockholms län","UV-relining, BRF-projekt","2009"),
 ("vastkust-rorinfodring","Västkust Rörinfodring","Göteborg","Västra Götalands län","Strumpmetoden, rörinspektion","2013"),
 ("osunds-relining","Öresund Relining","Malmö","Skåne län","Strumpmetoden, gjutjärn","2015"),
 ("mellansvensk-avlopp","Mellansvensk Avloppsteknik","Örebro","Örebro län","Högtryckspolning, UV-relining","2010"),
 ("norrlands-rorrenovering","Norrlands Rörrenovering AB","Umeå","Västerbottens län","Strumpmetoden, ventilation","2011"),
 ("uppsala-rorteknik","Uppsala Rörteknik","Uppsala","Uppsala län","UV-relining, gjutjärn","2016"),
 ("ostgota-stamservice","Östgöta Stamservice","Linköping","Östergötlands län","Strumpmetoden, spolning","2012"),
 ("smalands-rorinfodring","Smålands Rörinfodring","Jönköping","Jönköpings län","Strumpmetoden, rörinspektion","2014"),
 ("varmlands-relining","Värmlands Relining AB","Karlstad","Värmlands län","UV-relining, villa","2017"),
 ("gavle-rorteknik","Gävle Rörteknik","Gävle","Gävleborgs län","Strumpmetoden, gjutjärn","2013"),
 ("halmstads-stamservice","Halmstads Stamservice","Halmstad","Hallands län","UV-relining, BRF","2015"),
 ("vaxjo-rorrenovering","Växjö Rörrenovering","Växjö","Kronobergs län","Strumpmetoden, spolning","2016"),
 ("blekinge-rorinfodring","Blekinge Rörinfodring","Karlskrona","Blekinge län","Strumpmetoden, inspektion","2014"),
 ("dalarnas-relining","Dalarnas Relining AB","Borlänge","Dalarnas län","UV-relining, gjutjärn","2012"),
 ("vasteras-rorteknik","Västerås Rörteknik AB","Västerås","Västmanlands län","Strumpmetoden, fastighet","2011"),
 ("sundsvalls-stamteknik","Sundsvalls Stamteknik","Sundsvall","Västernorrlands län","UV-relining, spolning","2013"),
 ("lulea-rorinfodring","Luleå Rörinfodring","Luleå","Norrbottens län","Strumpmetoden, rörinspektion","2015"),
 ("ostersunds-relining","Östersunds Relining AB","Östersund","Jämtlands län","UV-relining, villa","2016"),
 ("skaraborgs-rorteknik","Skaraborgs Rörteknik","Skövde","Västra Götalands län","Strumpmetoden, gjutjärn","2012"),
 ("kalmar-stamservice","Kalmar Stamservice","Kalmar","Kalmar län","UV-relining, BRF","2014"),
 ("norrkoping-rorrenovering","Norrköping Rörrenovering","Norrköping","Östergötlands län","Strumpmetoden, spolning","2013"),
 ("karlskoga-rorinfodring","Karlskoga Rörinfodring","Karlskoga","Örebro län","UV-relining, villa","2017"),
 ("ljusdals-rorteknik","Ljusdals Rörteknik","Ljusdal","Gävleborgs län","Strumpmetoden, inspektion","2015"),
 ("helsingborgs-stamservice","Helsingborgs Stamservice","Helsingborg","Skåne län","UV-relining, gjutjärn","2011"),
 ("trollhattans-relining","Trollhättans Relining AB","Trollhättan","Västra Götalands län","Strumpmetoden, fastighet","2014"),
 ("kristianstads-rorteknik","Kristianstads Rörteknik","Kristianstad","Skåne län","UV-relining, villa","2016"),
 ("vykort-norrkopings-rorinfodring","Östergötlands Rörinfodring","Motala","Östergötlands län","Strumpmetoden, spolning","2013"),
 ("sodermanlands-relining","Södermanlands Relining","Eskilstuna","Södermanlands län","UV-relining, gjutjärn","2012"),
 ("vastmanlands-stamteknik","Västmanlands Stamteknik","Köping","Västmanlands län","Strumpmetoden, BRF","2015"),
 ("nynashamns-rorrenovering","Nynäshamns Rörrenovering","Nynäshamn","Stockholms län","UV-relining, villa","2017"),
]

# -------- kommuner för tjänstesidorna (de 80 största orterna)
SERVICE_CITIES = [
 "stockholm","goteborg","malmo","uppsala","vasteras","orebro","linkoping","norrkoping","jonkoping",
 "helsingborg","sundsvall","umea","gavle","boras","sodertalje","eskilstuna","halmstad","vaxjo",
 "karlstad","falun","borlange","solna","lund","nacka","huddinge","taby","jarfalla","ostersund",
 "lulea","trollhattan","uddevalla","skovde","karlskrona","nykoping","kalmar","kristianstad",
 "varberg","landskrona","trelleborg","sandviken","enkoping","koping","katrineholm","motala",
 "skelleftea","pitea","ornskoldsvik","kungsbacka","sigtuna","vastervik","norttalje","lidkoping",
 "vanersborg","alingsas","falkenberg","tranas","mariestad","nassjo","vetlanda","varnamo",
 "ljungby","oskarhamn","hassleholm","ystad","vellinge","svedala","eslov","hoganas","angelholm",
 "strangnas","flen","sala","hallstahammar","fagersta","avesta","ludvika","mora","leksand",
 "hudiksvall","bollnas","soderhamn","harnosand",
]

_MUNI = {slug:(name,lan,areas) for slug,name,lan,areas in M.ALL}

def _area_clause(name, areas):
    if areas:
        return f" och kringliggande områden som {esc(', '.join(areas))}"
    return " och närliggande orter"

def build_service_cities():
    # ---- hubb: avloppsspolning
    cards = ''.join(f'<a class="pills" href="/avloppsspolning/{s}/">{esc(_MUNI[s][0])}</a>'
                    for s in SERVICE_CITIES if s in _MUNI)
    body = f'''<section class="hero"><div class="wrap narrow">
      {crumb_html([("Hem","/"),("Avloppsspolning","/avloppsspolning/")])}
      <h1 class="h1">Avloppsspolning i hela Sverige</h1>
      <p class="lead">Stopp i avloppet? Vi förmedlar lokala spolfirmor som löser stopp med högtryck och kamera. Välj din ort för pris och kontakt.</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få hjälp med stopp</a>
        <a class="btn btn-ghost btn-lg" href="/pris/avloppsspolning/">Se priser</a></div></div></section>
      <section><div class="wrap"><div class="pills rv">{cards}</div></div></section>'''
    write("/avloppsspolning/index.html", page("Avloppsspolning – hitta spolfirma i din kommun | Reliningkoll",
      "Avloppsspolning nära dig. Jämför lokala firmor, priser och vad som gäller vid stopp i avloppet. Välj din kommun.",
      "/avloppsspolning/", body, crumb=[("Hem","/"),("Avloppsspolning","/avloppsspolning/")]))

    # ---- hubb: rörinspektion
    cards2 = ''.join(f'<a class="pills" href="/rorinspektion/{s}/">{esc(_MUNI[s][0])}</a>'
                     for s in SERVICE_CITIES if s in _MUNI)
    body = f'''<section class="hero"><div class="wrap narrow">
      {crumb_html([("Hem","/"),("Rörinspektion","/rorinspektion/")])}
      <h1 class="h1">Rörinspektion med kamera</h1>
      <p class="lead">En kamera inspektion visar rörens skick innan du beställer åtgärd. Välj din ort för lokala firmor och pris.</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Boka inspektion</a>
        <a class="btn btn-ghost btn-lg" href="/pris/rorinspektion/">Se priser</a></div></div></section>
      <section><div class="wrap"><div class="pills rv">{cards2}</div></div></section>'''
    write("/rorinspektion/index.html", page("Rörinspektion – kamera inspektion av avlopp | Reliningkoll",
      "Rörinspektion med kamera i din kommun. Se rörens skick, pris och lokala firmor. Boka kostnadsfri bedömning.",
      "/rorinspektion/", body, crumb=[("Hem","/"),("Rörinspektion","/rorinspektion/")]))

    for slug in SERVICE_CITIES:
        if slug not in _MUNI: continue
        name, lan, areas = _MUNI[slug]
        ac = _area_clause(name, areas)
        others = [s for s in SERVICE_CITIES if s != slug and s in _MUNI][:12]
        links = ''.join(f'<a class="pills" href="/avloppsspolning/{s}/">{esc(_MUNI[s][0])}</a>' for s in others)

        # --- avloppsspolning
        p = f"/avloppsspolning/{slug}/"
        b = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Avloppsspolning","/avloppsspolning/"),(name,p)])}
          <h1 class="h1">Avloppsspolning i {esc(name)}</h1>
          <p class="lead">Stopp i avloppet i {esc(name)}? Vi förmedlar lokala spolfirmor i {esc(lan)} som löser stoppet med högtryck och kamera.</p>
          <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Få hjälp med stoppet</a>
            <a class="btn btn-ghost btn-lg" href="/pris/avloppsspolning/">Se priser</a></div></div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          <h2>Stopp i avloppet i {esc(name)}</h2>
          <p>Ett stopp i avloppet kommer sällan av en slump. Vanligast är fett och matrester i köket, hår i badrummet eller rötter som trängt in i utvändiga ledningar. Är stoppet återkommande är det ett tecken på att rören behöver ses över{ac}.</p>
          <p>Vi förmedlar firmor som arbetar i {esc(name)}{ac.replace(' och kringliggande områden som',' med omnejd, till exempel')}. Du beskriver ditt ärende en gång och får sedan hjälp snabbt.</p>
          <h2>Riktpriser i {esc(lan)}</h2>
          <table class="tbl" style="margin-bottom:24px"><thead><tr><th>Åtgärd</th><th>Riktpris</th></tr></thead><tbody>
            <tr><td>Rensning, enkel propp</td><td>800 – 1 800 kr</td></tr>
            <tr><td>Högtrycksspolning villa</td><td>1 500 – 3 500 kr</td></tr>
            <tr><td>Spolning flerbostadshus</td><td>3 000 – 6 000 kr</td></tr>
            <tr><td>Akut kväll/helg</td><td>2 000 – 5 000 kr</td></tr>
            <tr><td>Rörinspektion med kamera</td><td>0 – 2 500 kr</td></tr>
          </tbody></table>
          <div class="callout"><p>Återkommer stoppet är orsaken oftast avlagringar eller rötter. Då ger en rörinspektion svaret, och relining kan vara rätt lösning på sikt.</p></div>
          <h2>Så går det till i {esc(name)}</h2>
          <ol><li>Du beskriver stoppet och din adress i {esc(name)}.</li>
          <li>Vi skickar förfrågan till lokala spolfirmor.</li>
          <li>Du får hjälp med spolning och vid behov rörinspektion.</li></ol>
          <h2>Relining i {esc(name)}</h2>
          <p>Om stoppet beror på slitna rör kan relining vara ett billigare alternativ än att spola om och om igen. Läs mer om <a href="/relining/{slug}/">relining i {esc(name)}</a>.</p>
          <h2>Vanliga frågor om stopp i {esc(name)}</h2>
          <div class="faq">
            <details><summary>Vad kostar avloppsspolning i {esc(name)}?</summary><p>En spolning ligger vanligen mellan 1 500 och 3 500 kr beroende på omfattning och tidpunkt. Akut kväll eller helg kan kosta mer.</p></details>
            <details><summary>Kommer stoppet tillbaka?</summary><p>Är orsaken avlagringar eller rötter kommer stoppet ofta tillbaka. Då är rörinspektion och eventuell relining rätt åtgärd.</p></details>
            <details><summary>Kan jag lösa stoppet själv?</summary><p>Enkla proppar går att lösa med vaskrensare eller kokhett vatten. Sitter stoppet längre in krävs högtrycksspolning.</p></details>
          </div>
          <h2 style="font-size:22px">Avloppsspolning i fler orter</h2>
          <div class="pills rv">{links}</div>
          <div class="cta-band" style="margin-top:40px"><h2>Få hjälp med stoppet i {esc(name)}</h2>
            <p>Gratis och utan förpliktelse. Lokala firmor i {esc(lan)}.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Skicka förfrågan</a></div>
        </div></div></section>'''
        write(p+"index.html", page(f"Avloppsspolning {esc(name)} – pris och lokala firmor | Reliningkoll",
          f"Avloppsspolning i {name}? Hitta lokala spolfirmor i {lan}. Priser för stopp i avloppet och snabb hjälp med högtrycksspolning.",
          p, b, crumb=[("Hem","/"),("Avloppsspolning","/avloppsspolning/"),(name,p)]))

        # --- rörinspektion
        p2 = f"/rorinspektion/{slug}/"
        b2 = f'''<section class="hero"><div class="wrap narrow">
          {crumb_html([("Hem","/"),("Rörinspektion","/rorinspektion/"),(name,p2)])}
          <h1 class="h1">Rörinspektion i {esc(name)}</h1>
          <p class="lead">Beställ kamera inspektion av avloppsrör i {esc(name)}. Vi förmedlar lokala firmor i {esc(lan)} som dokumenterar rörens skick.</p>
          <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/offert/">Boka inspektion</a>
            <a class="btn btn-ghost btn-lg" href="/pris/rorinspektion/">Se priser</a></div></div></section>
        <section style="padding-top:0"><div class="wrap"><div class="prose">
          <h2>Vad en rörinspektion visar</h2>
          <p>Med en kamera inspekteras rören inifrån i {esc(name)}. Du ser rörens skick, dimension, eventuella sprickor, rötter och avlagringar. Det är grunden för varje seriös offert på relining eller spolning. Vi förmedlar lokala firmor i {esc(name)}{ac}.</p>
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
          <h2>Vanliga frågor om rörinspektion i {esc(name)}</h2>
          <div class="faq">
            <details><summary>Vad kostar en rörinspektion i {esc(name)}?</summary><p>För villa ligger den ofta mellan 0 och 2 500 kr, ibland gratis i samband med offert. För fastigheter är priset högre.</p></details>
            <details><summary>Får jag behålla filmen?</summary><p>Ja, du bör få både film och protokoll som dokumentation.</p></details>
            <details><summary>Är inspektion alltid nödvändig?</summary><p>För en korrekt offert, ja. Utan den blir priset en gissning.</p></details>
          </div>
          <div class="cta-band" style="margin-top:40px"><h2>Boka rörinspektion i {esc(name)}</h2>
            <p>Kostnadsfri bedömning av lokala firmor i {esc(lan)}.</p>
            <a class="btn btn-primary btn-lg" href="/offert/">Skicka förfrågan</a></div>
        </div></div></section>'''
        write(p2+"index.html", page(f"Rörinspektion {esc(name)} – kamera inspektion av avlopp | Reliningkoll",
          f"Rörinspektion i {name} med kamera. Hitta lokala firmor i {lan} och se priser för inspektion av avloppsrör.",
          p2, b2, crumb=[("Hem","/"),("Rörinspektion","/rorinspektion/"),(name,p2)]))

if __name__ == "__main__":
    build_service_cities()
    print("scale: tjänstesidor klara")
