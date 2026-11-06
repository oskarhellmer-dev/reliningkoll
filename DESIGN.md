# Design

<!-- impeccable:design-schema 1 -->

## Värld

**Besiktningsprotokollet.** Sajten läses som ett ifyllt, stämplat inspektionsdokument för avloppsrör — inte som en broschyr. Arkivpapper som grund, hårlinjer som struktur, fältrader som innehållsbärare, mätvärden i mono, och en stämpel som enda färghändelse.

Världen valdes för att den bär produktens mekanism: ett ärende som dokumenteras, bedöms och matchas. Den är anti-referens mot kategorins standard (mörkblå gradient, rundade kort med ikon, pill-knappar).

## Färg

Strategi: Restrained. Neutrala ytor ur världen plus en accent som gör ett verkligt jobb.

| Token | Värde | Roll |
|---|---|---|
| `--paper` | `#eceee7` | Kall grågrön arkivpärm. Medvetet inte grädde. |
| `--plate` | `#f4f5f1` | Blanketten — formulär, callouts, tabellrader |
| `--panel` | `#e2e5dc` | Förhöjd yta |
| `--ink` | `#14181a` | Text och struktur |
| `--ink-soft` | `#4c534d` | Sekundär text |
| `--ink-faint` | `#575e57` | Placeholder, markering |
| `--rule` | `#bcc2b7` | Hårlinje |
| `--rule-strong` | `#14181a` | Dokumentets ram |
| `--stamp` | `#17408f` | Stämpelblå — länkar, knappar, aktiva fält |
| `--signal` | `#9e2a1c` | Protokollröd — endast stämpel/status/fel |
| `--ok` | `#1e6a47` | Godkänd-markering |

Kontrast: brödtext ≥4,5:1, stor text ≥3:1. Verifierat av detektorn.

## Typografi

- **Display och brödtext:** Archivo (variabel, självhostad). Rubriker versala, vikt 800, spärrning −0,02 till −0,03em. Brödtext 17px/1,62, mått 66ch.
- **Data och fält:** Azeret Mono (variabel, självhostad). Versala etiketter, spärrning 0,03–0,14em. Används för mätvärden, fält, nav, brödsmulor, tabellhuvuden — aldrig som kostym.
- Tabellsiffror: `font-variant-numeric: tabular-nums` genomgående.

## Former

- Radie: 0–2px. Ingen rundad kort-estetik.
- Kant: 1px hårlinje (`--rule`) för avskiljning; 1px `--rule-strong` för dokumentets ram.
- Callout: ram + `box-shadow: inset 0 3px 0 var(--ink)` som överkant. Ingen `border-left`.
- Djup: endast inset-markering. Inga färgade glömskor, inga hårda offset-skuggor.

## Rörelse

**Ett** auktoriserat moment: stämpeln i heron trycks ned en gång (`stamp-press`, 0,62s, ease-out-expo). Allt annat står stilla. Inga utspridda scroll-reveals. `prefers-reduced-motion` stänger av momentet.

## Webbläsarytor

Markeringsfärg (stämpelblå/platte), `caret-color` stämpelblå, tunn scrollbar i papper/grågrönt, `:focus-visible` 2px stämpelblå med 3px offset, understrykning med `text-underline-offset: .18em`.

## Foto

Fotografier läses som **bilagor till protokollet** — ett foto som fästs på blanketten, inte en säljbild.

- Ram: 1px `--rule-strong`. Ingen rundning. Ligger på `--plate`.
- Bildtext: Azeret Mono, versal etikett (`Före` / `Efter`) + förklaring i `--ink-soft`, avskild med hårlinje överst.
- Före/efter: `.foto-pair` lägger två foton sida vid sida, delade av en hårlinje; staplas på smal skärm.
- Alla bilder: WebP med JPG-fallback, `width`/`height` (ingen CLS), `loading="lazy"`, `decoding="async"`.
- Inga logotyper, varumärken eller text i bilden. Dokumentär stil (35mm-känsla), inte glossy stock.
- Byggs med `foto()` / `foto_pair_block()` i `build_core.py`.

## Vad som inte får återinföras

Gradient-text · kicker/eyebrow ovanför rubrik · `border-left` >1px på kort/callouts · rundade kort med ikon+rubrik+text som sidstruktur · nästlade kort · grädde/beige bakgrund · Inter/Roboto/Space Grotesk · påhittade betyg eller recensioner.
