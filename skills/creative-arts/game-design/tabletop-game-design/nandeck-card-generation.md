---
id: creative-arts.game-design.tabletop-game-design.nandeck-card-generation
name: nandeck-card-generation
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, nandeck, paper-prototyping, data-merge, card-generation, prototype-cards, spreadsheet, csv, print-and-play]
level: practitioner
status: draft
description: "Generate prototype cards with nanDeck from a spreadsheet: link a CSV, place fields with RECTANGLE/FONT/TEXT, print sheets of poker cards, and iterate card data fast."
sources:
  - https://www.nandeck.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# nanDeck card generation

**Goal:** turn a card spreadsheet into printable prototype cards in minutes, so every
balance change is a spreadsheet edit plus a reprint.

nanDeck (Windows freeware by Andrea Nini) builds cards from a script and optional linked
data. The program's manual documents all directives; check it for exact syntax in your
version.

## Workflow
1. **Card data in a spreadsheet**: one row per card, columns for name, cost, type, text,
   count. Export to CSV (or link the spreadsheet directly where supported).
2. **Script** (example; verify directive details in the nanDeck manual):
```
; poker-size cards on A4, linked data
CARDSIZE = 6.35, 8.89
LINKMULTI = Count           ; repeat each row by the Count column
LINK = "cards.csv"
BORDER = RECTANGLE, #000000, 0.1
FONT = Arial, 14, B, #000000
TEXT = "1-{(Name)}", [Name], 0.3, 0.3, 5.75, 0.8, CENTER, CENTER
FONT = Arial, 9, , #000000
TEXT = "1-{(Name)}", [Text], 0.4, 4.5, 5.55, 3.5, CENTER, WWTOP
FONT = Arial, 20, B, #AA0000
TEXT = "1-{(Name)}", [Cost], 0.2, 0.2, 1, 1, CENTER, CENTER
```
   `[Field]` references a CSV column; `"1-{(Name)}"` applies to cards 1..number of rows.
3. **Validate** (nanDeck's Validate deck), **Build deck**, then **Print/PDF** - nanDeck
   lays cards onto pages automatically with your page setup.
4. Print, cut (paper trimmer), sleeve over regular cards for shuffle-ability.

## Tips
- Keep a `Version` column and print it small on each card so old prototype cards are
  identifiable.
- Use icons as image files referenced from a column (IMAGE directive).
- Start ugly; clarity over art in prototypes.
- Alternatives: Component Studio, Dextrous, Squib (Ruby), spreadsheet mail-merge in
  InDesign/Affinity; Tabletop Simulator can import deck sheets (see
  `creative-arts.game-design.tabletop-game-design.tabletop-simulator-prototyping`).

## Gotchas
- nanDeck is Windows-only (runs under Wine on other systems, with caveats).
- CSV delimiters and encoding (commas in rules text, accented characters) break links;
  quote fields and save as UTF-8 if supported.
- Long text auto-shrinks or overflows depending on settings; check the longest card.

## Verify
- [ ] Spreadsheet is the single source of card data.
- [ ] Script builds without validation errors.
- [ ] Printed sheet matches card size; version number visible.
