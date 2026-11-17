---
id: creative-arts.comics-and-sequential-art.manga.screentone-line-count-and-density
name: screentone-line-count-and-density
category: creative-arts
field: comics-and-sequential-art
product: manga
tags: [manga, screentone, manga-tones, tone-lpi, tone-density, lines-per-inch, halftone-dots, print-reduction]
level: practitioner
status: draft
description: "Choose screentone line count (LPI) and density for manga: common 50-70 LPI ranges, density percentages for skin, shadows and backgrounds, and print/reduction risks."
sources:
  - https://en.wikipedia.org/wiki/Screentone
  - https://en.wikipedia.org/wiki/Halftone
  - https://help.clip-studio.com/en-us/First_Topic.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screentone line count and density

**Goal:** tones that print cleanly, read as grey at reading distance, and stay
consistent across a volume.

## Two parameters
- **Line count (LPI / lines per inch)**: how fine the dot grid is. Higher = finer, more
  like smooth grey; lower = visible dots (graphic look).
- **Density (%)**: how much of the area is black. 10% light grey, 30% mid, 50%+ dark.

## Typical choices (commonly used ranges; magazine specs may differ)
- Line counts around **50-70 LPI** at manuscript size are common for general tones;
  ~60 LPI is a frequent default. Finer (80+) risks dots filling in or vanishing when
  reduced to small tankobon size; coarser (~27-42) gives a bold pop-art look.
- Density examples: 5-10% for skin/light shading, 20-30% for clothing and mid shadow,
  40-60% for darker shadows and night skies.
- Keep the **same LPI** across most of the book so tones don't moire when overlapped.

## Reduction
Manuscripts (B4) are reduced for print (B5 magazine, B6 tankobon). Fine LPI shrinks
further. Test-print a page at final size.

## Digital (Clip Studio Paint)
- Tone layers: set Frequency (LPI), Density, dot type (circle is standard), angle (45
  degrees common).
- Output at 600-1200 dpi as monochrome so dots render cleanly (tones at 350 dpi greyscale
  can alias).

## Gotchas
- Mixing LPIs in overlapping areas: moire.
- Tones over 70-80% density look nearly black and may clog in print.

## Verify
- [ ] Book-wide default LPI chosen; density palette listed in style notes.
- [ ] Test print at final reduced size shows clean dots.
