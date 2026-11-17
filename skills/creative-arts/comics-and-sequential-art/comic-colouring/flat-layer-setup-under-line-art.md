---
id: creative-arts.comics-and-sequential-art.comic-colouring.flat-layer-setup-under-line-art
name: flat-layer-setup-under-line-art
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, flatting, flats, flat-layer-setup, multiply-line-art, layer-structure, photoshop, clip-studio-paint]
level: practitioner
status: draft
description: "Set up a colour file for flatting: line art on a locked Multiply layer, flats layer below with no anti-aliasing, distinct flat colours per region, and a standard layer stack."
sources:
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
  - https://helpx.adobe.com/photoshop/using/blending-modes.html
  - https://help.clip-studio.com/en-us/First_Topic.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flat layer setup under line art

**Goal:** a file structure where flats are clean, selectable, and never damage the
line art.

## File setup
1. Open the line art (1-bit or greyscale) at working resolution (commonly 300-600 ppi
   at print size; match the publisher spec).
2. Convert to RGB (or CMYK if the publisher requires colouring in CMYK).
3. Move the line art to its own layer named `LINES`; blend mode **Multiply** so white
   becomes transparent; lock it.
   - Alternative: convert lines to a transparent layer (Select > Color Range white,
     delete) and keep it Normal on top.
4. Create `FLATS` below `LINES`. Optionally a `BG` white layer at the bottom.

## Standard stack (top to bottom)
```
SFX / FX
LINES (Multiply, locked)
RENDER (shading/lighting, clipped or Multiply/Screen layers)
FLATS (aliased, distinct colours)
BG (white)
```
Colourists receive FLATS + LINES from flatters; rendering happens on layers above
FLATS.

## Flat colour rules
- Every separate region that needs its own colour/selection gets a **distinct flat
  colour**, even if final colours will match (e.g. two characters' jackets).
- **No anti-aliasing** on flats: pencil tool or aliased lasso/bucket so magic-wand
  selections are exact.
- Fill under lines fully: flats extend to the middle of or under the line, leaving
  no white gaps.
- Flats are often deliberately garish or arbitrary; they're selection masks, not final
  colours (some colourists flat in rough final colours to save a step).

## Gotchas
- Line art not on Multiply: flats hide the lines.
- Anti-aliased flats: selections pick up fringes and leave halos.

## Verify
- [ ] LINES locked on Multiply above FLATS.
- [ ] Every region distinct, aliased, no white gaps at 200-300% zoom.
