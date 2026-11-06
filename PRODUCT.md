# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Svenska fastighetsägare med äldre avloppsrör. Tre grupper:
- **Villaägare** i hus byggda före 1970, där gjutjärnsrören rostat och ger återkommande stopp.
- **Bostadsrättsföreningar och fastighetsbolag** som behöver relina stammar utan att evakuera boende.
- **Husinköpare** som vill veta rörens skick innan köp.
Situationen: ett konkret problem (stopp, lukt, besiktning) som kräver en entreprenör. De söker lokalt, vet inte vad det kostar, och vill slippa ringa runt.

## Product Purpose

Reliningkoll är en oberoende jämförelsetjänst för relining, avloppsspolning och rörinspektion i Sverige. Besökaren beskriver sitt ärende en gång och matchas med upp till tre granskade lokala entreprenörer. Kostnadsfritt för privatpersoner, ingen bindningstid.
Framgång = kvalificerade förfrågningar som leder till offerter, och en sajt som rankar organiskt utan betald trafik.

## Positioning

Besökaren beskriver ärendet en gång och får offerter från upp till tre granskade firmor i sin kommun — i stället för att ringa runt. Sidorna är datadrivna med riktig SCB-statistik per kommun (bostadsbestånd, byggnadsperioder), vilket lokala konkurrenter saknar. Firmorna betalar per lead de accepterar; besökaren betalar inget och bindningen är noll.

## Operating Context

Svensk marknad. Avloppsrör i hus byggda före 1970 är i regel gjutjärn, som rostar inifrån. ROT-avdrag gäller arbetskostnaden i egen villa (30 %, tak 50 000 kr/person/år). Kommunala VA-huvudmän äger nätet fram till förbindelsepunkten. Entreprenörsmarknaden är fragmenterad (ca 163 bolag). Hög CPC på lokala sökord visar att firmor redan betalar för leads.

## Capabilities and Constraints

- Statisk HTML/CSS-sajt. Ingen backend. Formulär via formsubmit.co.
- 60 datadrivna kommunsidor (SCB), 48 tjänstesidor, guider, prissidor, firmaprofiler.
- Sökord i fokus: relining, relining avlopp, stopp i avlopp, avloppsspolning, rörinspektion.
- Domän ej registrerad ännu; förhandsversion på GitHub Pages.
- Teknisk krav: WCAG AA-kontrast (4,5:1 brödtext). Ingen påhittad data.

## Brand Commitments

Namnet Reliningkoll. Språk: svenska med korrekt ÅÄÖ. Oberoende röst: saklig, konkret, aldrig säljig eller hypig.
Bindande regel: fabricera aldrig recensioner, betyg eller kundcitat. Inga påhittade priser eller fakta — all statistik ska ha källa.

## Evidence on Hand

- Riktig kommunstatistik från SCB:s öppna API (`data/scb_bostad.json`, `data/scb_extra.json`): bostäder per hustyp, byggnadsperiod per årtionde, befolkning.
- Riktig sökvolym och CPC per ort (OpenSEO).
**Saknas och får inte hittas på:** inga anslutna firmor, inga kundomdömen, inga referensprojekt, inga påhittade betyg.

## Product Principles

1. Riktig data före utfyllnad — varje lokalt påstående ska kunna källhänvisas.
2. Oberoende framför sälj: besökaren ska kunna jämföra, inte övertalas.
3. Tjänar pengar på firmorna, aldrig på besökarens uppgifter.
4. Lokal relevans genom fakta, inte upprepning.

## Accessibility & Inclusion

WCAG AA-kontrast minst 4,5:1 för brödtext, 3:1 för stor text. Tangentbordsnavigering, synlig fokusmarkering, `prefers-reduced-motion` respekteras.
