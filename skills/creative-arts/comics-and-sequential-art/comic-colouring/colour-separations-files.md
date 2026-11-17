---
id: creative-arts.comics-and-sequential-art.comic-colouring.colour-separations-files
name: colour-separations-files
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, colour-separations, colour-holds]
level: advanced
status: draft
description: "Prepare colour separations for comic print: CMYK plates, black line art on a separate overprinting plate, holds, trapping and rich black, and checking each plate before delivery."
sources:
  - https://books.google.com/books?vid=ISBN9780823010301
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
  - https://en.wikipedia.org/wiki/Color_separation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Colour separations files

**Goal:** print-ready colour files where each plate is correct and black line art
overprints cleanly.

## Background
Historic comics were separated by hand (Ben-Day percentages on acetates). Today
"separations" means a CMYK file built so line art and colour do not misregister.

## Build
1. Line art: 1-bit or greyscale at 600 ppi, placed on the black (K) plate only,
   100 percent K, overprint (Multiply in Photoshop).
2. Colour: CMYK flats and rendering beneath, usually 300-400 ppi.
3. Colour holds: process colour builds, not K.
4. Black fills in the art: 100K line art over a colour underlayer, or rich black
   (e.g. C40 M30 Y30 K100) for large solid areas per printer spec; keep text
   and fine lines pure K.
5. Total ink limit: per printer (often 240-300 percent for uncoated or 300-320
   percent for coated).

## Check each plate
- Photoshop Channels: view C, M, Y, K individually. K plate should contain line
  art; no stray colour under thin lines unless intended.
- Look for knockout white gaps under lines (trapping errors).
- Ink coverage readout with the Info palette total ink.

## Deliver
- Layered TIFF or PSD per printer spec (lines as separate layer if asked), or a
  flattened CMYK TIFF / PDF/X-1a.

## Verify
- [ ] K plate contains all line art at 100K.
- [ ] Maximum ink coverage within the printer's limit.
