#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Djupa, unika guider - sajtens riktiga vallgrav. Ingen geo-mall, bara vardefullt innehall."""
import sys
sys.path.insert(0, "/home/clawd/reliningkoll")
from build_part1 import sec, ul

G = {}

G["relining-av-badrum"] = {
 "h1":"Relining av badrum – när och hur",
 "title":"Relining av badrum – avlopp utan att riva | Reliningkoll",
 "desc":"Relining av badrum förnyar avloppsstammen under kaklet utan att badrummet rivs. Här är när det är möjligt, vad det kostar och vad du bör kontrollera.",
 "body": sec("Varför badrummet är den känsligaste delen", [
   "Badrummets avlopp är det mest belastade i huset: dusch, tvättställ, toalett och golvbrunn möts i samma stam, och rören är ofta av gjutjärn i äldre hus. Det är också här läckage gör mest skada, eftersom vattnet söker sig ned i bjälklaget och in i underliggande lägenhet."]) +
 sec("Kan man relina utan att riva?", [
   "Ja. Poängen med relining är att röret förnyas inifrån via en servicelucka eller golvbrunnen, utan att kakel och tätskikt tas bort. Arbetet kräver dock åtkomst och att golvbrunnar och anslutningar öppnas upp efteråt."]) +
 sec("Så görs det", []) + ul([
   "Kamera inspektion av stammen och samtliga anslutningar.",
   "Rören högtrycksspolas och slipas rena invändigt.",
   "Fodret förs in och härdas mot rörväggen.",
   "Golvbrunn, toalettanslutning och tvättställsgren öppnas upp med robot.",
   "Ny kamera inspektion dokumenterar resultatet."]) +
 sec("Vad det kostar", [
   "Relining av en enskild badrumsstam ligger vanligen mellan 25 000 och 60 000 kr beroende på längd och antal anslutningar. I en villa med flera badrum kan kostnaden öka, men den är fortfarande klart lägre än att riva och bygga nytt."]) +
 sec("När badrummet måste rivas ändå", [
   "Är rören kollapsade, om golvbrunnen saknar godkänd tätning eller om tätskiktet är uttjänt kan relining inte rädda helheten. Då är åtgärden att bygga om badrummet, och relining av stammen kan bli ett led i det arbetet."]) +
 sec("Kontrollera detta i offerten", [
   "Att anslutningar och golvbrunnar ingår, att dokumentation före och efter lämnas, vilket foder som används och att garanti skrivs skriftligt. En offert som inte nämner anslutningarna är ofta missvisande låg."]),
 "faq":[("Måste kaklet bort vid relining?","Nej, en korrekt utförd relining görs via servicelucka eller golvbrunn utan att kakel och tätskikt rivs."),
        ("Hur lång tid tar det?","En badrumsstam tar oftast en till två dagar. Vattnet kan vara avstängt några timmar under härdningen."),
        ("Kan jag använda badrummet under tiden?","Ja, med undantag för de timmar då fodret härdas.")]}

G["relining-av-kok"] = {
 "h1":"Relining av köksavlopp",
 "title":"Relining av kök – avlopp, fett och stopp | Reliningkoll",
 "desc":"Köksavloppet drabbas hårdast av fett och matrester. Relining av köksavlopp ger ett slätt rör som inte bygger beläggning.",
 "body": sec("Varför köket får stopp först", [
   "Ingen annanstans i huset spolas så mycket fett, matrester och tvål ned som i köket. I gamla gjutjärnsrör fastnar det i den rostiga ytan och bildar en beläggning som långsamt stryper flödet. Resultatet blir återkommande stopp som blir tätare för varje gång."]) +
 sec("Vad relining gör skillnad med", []) + ul([
   "Röret blir slätt och fett fastnar inte på samma sätt.",
   "Rost och avlagringar försvinner bort.",
   "Ingen rivning av köksinredning eller golv.",
   "Livslängd 40 till 50 år vid korrekt utförande."]) +
 sec("Alternativet till relining", [
   "Att spola köksavloppet löser stoppet här och nu, men inte orsaken. Återkommer stoppet flera gånger per år är det billigare att relina röret en gång än att spola om och om igen."]) +
 sec("Bra att veta", [
   "Fett ska aldrig hällas ut i avloppet, oavsett rörtyp. Även i ett nytt, slätt rör stelnar fett och bygger upp beläggning över tid."]),
 "faq":[("Kan man relina bara köksavloppet?","Ja, enskilda grenar kan relinas separat om stammen i övrigt är frisk."),
        ("Fastnar fett i ett relinat rör?","Mycket mindre än i ett rostigt gjutjärnsrör, eftersom ytan är slät.")]}

G["relining-av-tvattstuga"] = {
 "h1":"Relining av tvättstugans avlopp",
 "title":"Relining tvättstuga – ludder, stopp och rör | Reliningkoll",
 "desc":"Tvättmaskin och torktumlare belastar avloppet med ludder och fiber. Relining av tvättstugans avlopp minskar återkommande stopp.",
 "body": sec("Varför tvättstugan får problem", [
   "Tvättmaskinen spolar ut ludder, fiber och tvålrester som klumpar ihop sig i röret. I äldre gjutjärnsrör med rostig insida fastnar luddet särskilt lätt och bildar proppar som växer sig allt större."]) +
 sec("Lösningar i ordning", []) + ul([
   "Rengör vattenlås och kontrollera fallet på avloppsslangen.",
   "Spola röret med högtryck för att få bort beläggning.",
   "Vid återkommande stopp: kamera inspektion.",
   "Är röret slitet invändigt: relining ger en slät yta där luddet inte fäster."]) +
 sec("Var du placerar maskinen", [
   "En tvättmaskin som står långt från stammen får en lång, svag avloppsväg där avlagringar lättare byggs upp. Placera den nära stammen där det går."]),
 "faq":[("Är relining värt det för en tvättstuga?","Ja, om stoppet återkommer trots rengöring. Ett slätt rör löser orsaken, inte bara symtomet."),
        ("Kan man spola själv?","Vattenlåset går att rengöra själv, men beläggning längre in i röret kräver högtrycksspolning.")]}

G["relining-av-kallare"] = {
 "h1":"Relining av källaravlopp",
 "title":"Relining av källare – avlopp under marknivå | Reliningkoll",
 "desc":"Källaravlopp ligger under uppstigningsnivån och drabbas hårdast av stopp och bakvatten. Så fungerar relining i källaren.",
 "body": sec("Källarens särskilda problem", [
   "Avlopp i källaren ligger under gatunivån. Vid stopp eller uppdämning i det kommunala nätet trycker vatten upp i källaravloppet först. Dessutom är rören i källaren ofta de äldsta i huset, ofta av gjutjärn från tidigt 1900-tal."]) +
 sec("Vad relining löser och inte", []) + ul([
   "Löser: slitna, rostiga och otäta rör i källaren.",
   "Löser: upprepade stopp i källargrenar.",
   "Löser inte: bakvatten från det kommunala nätet (det kräver backventil).",
   "Löser inte: grundvatten och fuktproblem utanför röret."]) +
 sec("Kombinera med backventil", [
   "Har du källare bör relining av de slitna rören kombineras med en backventil som stänger om flödet vänder. Det är den billigaste försäkringen mot översvämning i källaren."]) +
 sec("Kontrollera först", [
   "Innan relining i källaren bör en kamera inspektion visa att rören är hela nog. Har rören tappat fall eller är kollapsade behövs ett byte i stället."]),
 "faq":[("Kan man relina källarrör under betonggolv?","Ja, det är en av metodens stora fördelar – ingen bilning av golvet behövs."),
        ("Hindrar relining bakvatten?","Nej, det kräver en backventil. Relining hindrar inte vatten från att tränga upp bakvägen.")]}

G["relining-av-radhus"] = {
 "h1":"Relining av radhus",
 "title":"Relining av radhus – gemensamma stammar | Reliningkoll",
 "desc":"I radhus delar flera hushåll på avloppssystemet. Här är vad som gäller vid relining av gemensamma stammar, vem som ansvarar och vad det kostar.",
 "body": sec("Radhusets speciella förutsättningar", [
   "I ett radhus löper ofta en gemensam stam under hela längan. Varje hushåll har sina egna grenar, men huvudledningen delas. Det innebär att relining av en del kan kräva samordning med grannarna och att ansvaret regleras i stadgar eller gemensamhetsanläggning."]) +
 sec("Vem ansvarar för vad", []) + ul([
   "Egen gren in till huset: normalt ditt ansvar.",
   "Gemensam stam under längan: ofta gemensamhetsanläggning eller förening.",
   "Tomt- eller servisledning ut till gatan: varierar, kontrollera med kommunen.",
   "Först ut i längan har ofta ansvaret för rör ända fram till förbindelsepunkten."]) +
 sec("Så lägger du upp arbetet", [
   "Börja med en gemensam inspektion av hela stammen för att se om problemet är lokalt eller delat. Är det delat blir det billigare per hushåll att relina hela längan i ett svep än att varje hushåll gör det separat."]) +
 sec("Kostnad", [
   "En gemensam stam delas normalt efter antal hushåll. Att relina hela längan samtidigt ger lägre styckpris eftersom etablering och inspektion delas."]),
 "faq":[("Måste grannarna vara med?","Ofta ja, om stammen är gemensam. Börja med att reda ut ägandet via stadgar eller kommunen."),
        ("Kan jag relina bara min del?","Om din gren är separat, ja. Är stammen gemensam bör hela åtgärdas samtidigt.")]}

G["relining-av-fritidshus"] = {
 "h1":"Relining av fritidshus och sommarstuga",
 "title":"Relining fritidshus – avlopp i stugan | Reliningkoll",
 "desc":"Fritidshus har ofta gamla gjutjärnsrör som står oanvända stora delar av året. Så avgör du om relining är rätt, och vilka hänsyn som gäller.",
 "body": sec("Varför fritidshus ofta behöver åtgärdas", [
   "Äldre sommarstugor har ofta avlopp från mitten av 1900-talet, med gjutjärnsrör som stått torra långa perioder. Kombinationen av ålder, fuktvandring och stillestånd gör rören sköra."]) +
 sec("Särskilda hänsyn", []) + ul([
   "Kamera inspektion behövs innan du beställer – rören kan vara skörare än de ser ut.",
   "Vintern innebär frostrisk, så arbetet planeras till barmark.",
   "Vissa fritidshus har inte godkänt avlopp alls och kräver annan lösning.",
   "Kontrollera kommunens krav innan åtgärd."]) +
 sec("Alternativ när rören är för skadade", [
   "I vissa fritidshus är rören så pass dåliga att en helt ny, enklare avloppslösning är mer rimlig än relining. En inspektion ger svaret."]),
 "faq":[("Kan man relina i ett ouppvärmt hus?","Arbetet görs under barmarkssäsong. Själva härdningen påverkas av temperatur och planeras därefter."),
        ("Måste kommunen godkänna?","Kontrollera kommunens regler för enskilda avlopp innan du beställer åtgärden.")]}

G["uv-hardning"] = {
 "h1":"UV-härdning av relining – så fungerar det",
 "title":"UV-härdning relining – metod och fördelar | Reliningkoll",
 "desc":"UV-härdning är en snabb reliningmetod där fodret härdas med ultraviolett ljus. Här är hur det fungerar och varför det används.",
 "body": sec("Vad UV-härdning är", [
   "Vid UV-relining används ett foder av glasfiber mättat med ljus-härdande plast. Fodret förs in i röret, blåses upp mot rörväggen och härdas snabbt av en UV-lampa som dras genom röret. Resultatet är ett nytt, skarvfritt rör."]) +
 sec("Fördelar", []) + ul([
   "Snabb härdning – klart på minuter till timmar per rör.",
   "Ingen värme eller vatten behövs för härdningen.",
   "Jämn kvalitet eftersom härdningen sker kontrollerat.",
   "Mindre påverkan på omgivningen än varmvattenhärdning."]) +
 sec("När metoden passar", [
   "UV är vanligt i stammar och längre ledningar, särskilt i flerbostadshus där arbetet behöver gå snabbt och störa så lite som möjligt."]) +
 sec("Jämfört med strumpmetoden", [
   "Strumpmetoden härdas vanligen med varmt vatten eller ånga och tar längre tid. UV ger snabbare härdning men kräver särskild utrustning, vilket inte alla entreprenörer har."]),
 "faq":[("Håller UV-relining lika länge?","Ja, livslängden anges normalt till 40 till 50 år, samma som andra reliningmetoder."),
        ("Är UV farligt?","UV-ljuset hanteras av utbildad personal med skyddsutrustning. För boende innebär metoden ingen risk.")]}

G["vilken-metod-ar-bast"] = {
 "h1":"Vilken reliningmetod är bäst?",
 "title":"Vilken reliningmetod är bäst? UV vs strumpa | Reliningkoll",
 "desc":"UV-härdning eller strumpmetoden? Här jämförs metoderna sida vid sida så att du kan bedöma vilken som passar just din fastighet bäst.",
 "body": sec("Svaret: det beror på röret", [
   "Det finns ingen metod som alltid är bäst. Valet styrs av rörets dimension, längd, krökar, material och hur snabbt arbetet måste gå. En erfaren entreprenör väljer metod efter en kamera inspektion."]) +
 '<table class="tbl"><thead><tr><th>Aspekt</th><th>UV-härdning</th><th>Strumpmetoden</th></tr></thead><tbody>' +
 '<tr><td>Härdningstid</td><td>Minuter till timmar</td><td>Timmar</td></tr>' +
 '<tr><td>Utrustning</td><td>UV-lampa och styrenhet</td><td>Värme/vatten eller ånga</td></tr>' +
 '<tr><td>Vanligast i</td><td>Stammar, längre ledningar</td><td>Villa, krökar</td></tr>' +
 '<tr><td>Livslängd</td><td>40–50 år</td><td>40–50 år</td></tr></tbody></table>' +
 sec("Vad du bör fråga entreprenören", [
   "Vilken metod de avser använda och varför, vilket foder som ingår och vilken garanti de lämnar. En seriös entreprenör kan förklara valet utifrån just dina rör."]),
 "faq":[("Ger den ena metoden bättre resultat?","Båda ger lång livslängd när de utförs rätt. Metodvalet handlar mer om rörets förutsättningar och omständigheterna på plats."),
        ("Kan man byta metod mitt i?","Nej, metoden bestäms utifrån inspektionen innan arbetet börjar.")]}

G["relining-fore-kop-av-hus"] = {
 "h1":"Relining innan du köper hus – vad du bör kontrollera",
 "title":"Köpa hus med gjutjärnsrör – relining och besiktning | Reliningkoll",
 "desc":"Gjutjärnsrör är en vanlig dold kostnad vid husköp. Så bedömer du rörens skick innan köpet, och vad relining kostar om den behövs.",
 "body": sec("Varför rören är en dold kostnad", [
   "Vid en vanlig besiktning kontrolleras sällan avloppets insida. Köper du ett hus byggt före 1970 är chansen stor att stammen är av gjutjärn, och att den behöver ses över inom några år. Det kan bli en kostnad på 100 000 kr eller mer som inte syns i annonsen."]) +
 sec("Så tar du reda på skicket", []) + ul([
   "Beställ en separat rörinspektion med kamera före köpet.",
   "Be om ålder på huset och om det finns dokumentation av tidigare rörarbeten.",
   "Kontrollera om stammen är gjutjärn, betong eller plast.",
   "Fråga säljaren om tidigare stopp eller spolning."]) +
 sec("Vad rören betyder för priset", [
   "Behöver stammen relinas kan det motivera ett prut. Beställ offert innan köpet och använd den som underlag i förhandlingen i stället för att gissa."]) +
 sec("Relining efter köpet", [
   "Är rören slitna men hela kan relining göras efter tillträdet utan att du flyttar in i ett byggkaos. Arbetet tar några dagar och kräver ingen rivning."]),
 "faq":[("Ingår avloppet i en vanlig besiktning?","Sällan invändigt. Beställ en egen rörinspektion för att veta rörens skick."),
        ("Kan jag kräva säljaren på åtgärden?","Det beror på avtalet och vad som varit känt. En inspektion före köp ger dig underlag att förhandla med.")]}

G["avloppsrens-sjalv"] = {
 "h1":"Rensa avloppet själv – vad som funkar och inte",
 "title":"Rensa avlopp själv – metoder och varningar | Reliningkoll",
 "desc":"Vaskrensare, avloppsrens eller högtryck? Här är vad du kan göra själv vid stopp i avloppet, vad som kan skada rören och när du bör ringa proffs.",
 "body": sec("Vad som fungerar", []) + ul([
   "Vaskrensare eller rensvajer – bäst vid hår och tvålrester i vattenlåset.",
   "Kokhett vatten i omgångar – löser fett i köket.",
   "Demontera och rengör vattenlåset – ofta där proppen sitter.",
   "Enzymbaserat avloppsrens – skonsamt mot rör och miljö."]) +
 sec("Vad som kan skada", [
   "Starka kemiska avloppsrens kan skada äldre gjutjärnsrör och täta rörledningar, och de är farliga att blanda med varandra. Undvik dem särskilt i hus med gamla rör."]) +
 sec("När du ska sluta försöka själv", [
   "Sitter stoppet längre in än vattenlåset, eller återkommer det snabbt, krävs högtrycksspolning med kamera. Fortsätter du med kemikalier riskerar du att skada rören utan att lösa orsaken."]) +
 sec("Förebygg", [
   "Sil i vasken, inget fett i avloppet och förebyggande spolning vartannat till var femte år minskar risken för stopp betydligt."]),
 "faq":[("Hjälper avloppsrens mot allt?","Nej. Kemiskt rens löser mjuk smuts men inte rötter eller hårda avlagringar."),
        ("Hur vet jag om stoppet sitter djupt?","Om flera avlopp påverkas samtidigt, eller om vaskrensaren inte når, sitter det i stammen.")]}

G["rut-eller-rot-avdrag"] = {
 "h1":"ROT eller RUT – vad gäller för avloppsarbete?",
 "title":"ROT vs RUT för avlopp och relining | Reliningkoll",
 "desc":"Relining och rörarbete i villa omfattas av ROT-avdraget, inte RUT. Här är skillnaden, taket och räkneexempel för dig som ska relina avlopp.",
 "body": sec("Skillnaden i korthet", [
   "ROT gäller reparation, underhåll och ombyggnad av din bostad, och omfattar rörarbete som relining. RUT gäller hushållsnära tjänster som städning och trädgård. Avloppsarbete hör alltså under ROT."]) +
 '<table class="tbl"><thead><tr><th></th><th>ROT</th><th>RUT</th></tr></thead><tbody>' +
 '<tr><td>Gäller</td><td>Rör, relining, bygg</td><td>Städ, trädgård, flytt</td></tr>' +
 '<tr><td>Avdrag</td><td>30 % av arbetskostnad</td><td>50 % av arbetskostnad</td></tr>' +
 '<tr><td>Tak per person/år</td><td>50 000 kr</td><td>75 000 kr</td></tr></tbody></table>' +
 sec("Vad som är avdragsgillt", [
   "Arbetskostnaden är avdragsgill, materialet inte. Be entreprenören specificera arbete och material separat i offerten så att du ser vad avdraget beräknas på."]) +
 sec("Krav", [
   "Du ska äga och bo i bostaden. Bostadsrätt och hyresrätt omfattas inte av ROT för relining av stammen, eftersom den tillhör föreningen."]),
 "faq":[("Kan jag använda ROT och RUT samma år?","Ja, det finns separata tak för ROT och RUT."),
        ("Gäller ROT för avloppsspolning?","Ja, arbetskostnaden för rörarbete i egen villa är ROT-berättigad.")]}

G["relining-av-huvudledning"] = {
 "h1":"Relining av huvudledning och servisledning",
 "title":"Relining av servisledning och huvudledning | Reliningkoll",
 "desc":"Servisledningen mellan huset och gatan kan också relinas. Här är vad som gäller för ledningar utanför huset, ansvarsfördelning och priser per meter.",
 "body": sec("Vilka ledningar det gäller", [
   "Servisledningen går från huset ut till kommunens förbindelsepunkt, ofta vid tomtgränsen. Den är normalt fastighetsägarens ansvar och kan precis som stammen relinas i stället för att grävas upp."]) +
 sec("Varför relining slår grävning", [
   "Att gräva upp en servisledning genom trädgård, uppfart och eventuell asfalt är dyrt och förstör marken. Relining sker via brunnar och befintliga öppningar utan schaktning."]) +
 sec("Vad som kontrolleras först", []) + ul([
   "Kamera inspektion av hela ledningen.",
   "Rörens fall och eventuella rotinträngningar.",
   "Var förbindelsepunkten med kommunens nät ligger.",
   "Ansvarsfördelningen mellan fastighetsägare och kommun."]) +
 sec("Kostnad", [
   "Servisledningar relinas ofta per meter, och priset påverkas av längd, dimension och åtkomst via brunnar."]),
 "faq":[("Vem äger servisledningen?","Normalt fastighetsägaren fram till kommunens förbindelsepunkt. Kontrollera med din kommun."),
        ("Kan rötter i ledningen åtgärdas?","Rötterna spolas bort och relining hindrar dem från att tränga in igen.")]}

G["relining-av-dagvatten"] = {
 "h1":"Relining av dagvattenledningar",
 "title":"Relining av dagvatten – dränering och stuprör | Reliningkoll",
 "desc":"Dagvattenledningar tar hand om regn och smältvatten från tak och dränering. Här är när relining är rätt och vad som skiljer från spillvatten.",
 "body": sec("Vad dagvattenledningar gör", [
   "Dagvattenledningar leder bort regn- och smältvatten från tak, uppfarter och dränering. De ligger ofta i mark, är av betong eller plast och kan precis som spillvattenledningar relinas."]) +
 sec("När de behöver åtgärdas", []) + ul([
   "Sprickor och vittrade fogar i betongrör.",
   "Rotinträngning från träd i närheten.",
   "Sättningar som gett fel fall och stående vatten.",
   "Översvämning vid kraftig nederbörd."]) +
 sec("Skillnaden mot spillvatten", [
   "Dagvatten är orenat regnvatten, vilket gör kraven och materialen något annorlunda. Metoden är dock densamma: röret förnyas inifrån utan schaktning."]) +
 sec("Kombinera med dränering", [
   "Har du fuktproblem i källaren kan problemet sitta i dagvatten- eller dräneringsledningen. En inspektion visar om relining räcker eller om dräneringen behöver göras om."]),
 "faq":[("Kan dagvattenledningar relinas?","Ja, samma princip används. Åtkomst via brunnar avgör hur arbetet läggs upp."),
        ("Löser relining fukt i källaren?","Om orsaken är en trasig dagvattenledning, ja. Är problemet grundvatten krävs annan åtgärd.")]}

G["hur-vet-man-att-ror-ar-gjutjarror"] = {
 "h1":"Hur vet man att rören är av gjutjärn?",
 "title":"Gjutjärnsrör eller plast – så känner du igen dem | Reliningkoll",
 "desc":"Osäker på om dina rör är gjutjärn eller plast? Här är hur du känner igen materialet utifrån husets ålder och vad det betyder för åtgärden.",
 "body": sec("Varför materialet spelar roll", [
   "Gjutjärnsrör rostar inifrån och behöver med tiden relinas eller bytas. Plaströr åldras långsammare men kan bli spröda. Vilket material du har avgör vilken åtgärd som är rimlig."]) +
 sec("Så känner du igen gjutjärn", []) + ul([
   "Mörk, gråsvart yta med tydlig metallkänsla.",
   "Tunga rör med gjutna skarvar eller muffar.",
   "Rost och avlagringar syns vid öppningar och i golvbrunnar.",
   "Vanligt i hus byggda före 1970."]) +
 sec("Så känner du igen plast", []) + ul([
   "Ljusgrå eller vit yta, lättare rör.",
   "Skarvade med muffar och gummiringar.",
   "Vanligt i hus byggda efter 1970-talet."]) +
 sec("Säkraste sättet", [
   "En kamera inspektion visar materialet och skicket invändigt, vilket är det enda tillförlitliga sättet att veta hur rören mår."]),
 "faq":[("Kan man se materialet utifrån?","Ibland, vid synliga rör i källare eller vid golvbrunnen. Annars krävs inspektion."),
        ("Måste jag veta materialet?","Det hjälper dig bedöma om och när åtgärd kan bli aktuell, men inspektionen är avgörande.")]}

G["avloppsror-dimensioner"] = {
 "h1":"Avloppsrörens dimension – vad siffrorna betyder",
 "title":"Avloppsrör dimensioner – så läser du måtten | Reliningkoll",
 "desc":"Vad betyder 110, 75 och 50 i avloppssammanhang? Här är rörens dimensioner och varför de spelar roll när du ska relina eller byta avloppsrör.",
 "body": sec("Varför dimensionen är viktig", [
   "Rörets innerdiameter avgör hur mycket vatten det klarar. Vid relining läggs ett foder inuti röret, vilket minskar innerdiametern något. Är röret nära sina gränser från början måste detta räknas in."]) +
 sec("Vanliga dimensioner", []) + ul([
   "110 mm – stam och avlopp från toalett.",
   "75 mm – avlopp från tvättställ och dusch.",
   "50 mm – klenare ledningar som tvättmaskin.",
   "160–200 mm – utvändiga servis- och huvudledningar."]) +
 sec("Vad relining gör med dimensionen", [
   "Fodret är tunt men minskar innerdiametern. I normala fall påverkar det inte funktionen, men i hårt belastade eller undermåligt dimensionerade system kan entreprenören behöva bedöma saken särskilt."]) +
 sec("Fråga om detta", [
   "Be entreprenören redogöra för hur rörets innerdiameter påverkas i just din fastighet. Det är en rimlig fråga och ett tecken på ett seriöst upplägg."]),
 "faq":[("Blir röret för trångt efter relining?","I normala fall nej. Entreprenören bedömer dimensionen utifrån inspektionen."),
        ("Vilken dimension har en stam?","Vanligast 110 mm i bostäder, men äldre hus kan ha andra mått.")]}

G["vad-ingar-i-en-relining"] = {
 "h1":"Vad ingår egentligen i en relining?",
 "title":"Vad ingår i en relining? Så läser du offerten | Reliningkoll",
 "desc":"Vad ska ingå i en relining och vad är tillval? Här är alla moment steg för steg, så att du kan jämföra offerter på lika villkor.",
 "body": sec("Momenten som ingår i en seriös relining", []) + ul([
   "Kamera inspektion före arbetet.",
   "Högtrycksspolning och nedslipning av rörens insida.",
   "Foder, införing och härdning.",
   "Upptagning och tätning av anslutningar och golvbrunnar.",
   "Kamera inspektion efter arbetet.",
   "Skriftlig dokumentation och garanti."]) +
 sec("Detta är ofta tillval", []) + ul([
   "Återställande av ytskikt efter ingrepp.",
   "Schaktning eller grävarbete vid utvändiga ledningar.",
   "Byte av golvbrunn.",
   "Extra insatser vid oväntade hinder i röret."]) +
 sec("Så jämför du offerter rätt", [
   "Två offerter som skiljer sig kraftigt i pris omfattar sällan samma saker. Jämför punkt för punkt mot listan ovan. En låg offert som saknar inspektion eller dokumentation är inte billigare – den är ofullständig."]) +
 sec("Rött att kräva", [
   "Dokumentation före och efter, uppgift om foder och metod, skriftlig garanti samt tydlig prisbild utan dolda tillägg."]),
 "faq":[("Ingår inspektion alltid?","I en seriös offert, ja. En offert utan inspektion är en gissning."),
        ("Kan priset ändras under arbetet?","Vid oväntade hinder, som kollapsade rör, kan tillägg bli nödvändiga. Be om att sådant regleras skriftligt i förväg.")]}
