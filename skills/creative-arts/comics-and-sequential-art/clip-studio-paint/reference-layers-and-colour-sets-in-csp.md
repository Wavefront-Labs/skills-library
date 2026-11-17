---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.reference-layers-and-colour-sets-in-csp
name: reference-layers-and-colour-sets-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-colouring, csp-reference-layer, csp-color-set, flatting, fill-tool, character-palette]
level: intro
status: draft
description: "Flat comic art accurately in Clip Studio Paint: set line art as reference layer for fills, close gap options, and build colour set palettes per character for consistency."
sources:
  - https://books.google.com/books?vid=ISBN9780823010301
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reference layers and colour sets

## Reference layer
- In the Layer palette select the line art layer and click **Set as reference layer** (lighthouse icon).
- Fill tool (or Auto select) > Tool property > **Refer**: "Reference layer" so fills on a separate colour
  layer stop at the line art.
- **Close gap** setting closes small breaks in the lines; **Area scaling** expands the fill under lines
  to avoid white halos (1-2 px typical at 600 dpi line art).
- Use "Fill > Enclose and fill" or "Paint unfilled area" sub tools to catch slivers.

## Colour sets
- **Window > Color set** palette. Create a new set per series or per character (+ add current colour).
- Name colours ("Hero skin", "Hero hair shadow") via the palette settings.
- Import/export colour sets, or download from Assets, for sharing with colour assistants.
- Use the eyedropper only on flats, not shaded areas, to keep flats exact.

## Flatting workflow
1. Line art layer = reference.
2. Flats layer below line art, colour by colour from the colour set.
3. Lock transparent pixels on flats layer for shading, or clip shade layers.

## Gotchas
- Fills that reference "All layers" pick up text and tones; use reference layer instead.
- Anti-aliased line art fills leave fringe pixels; use area scaling or "Fill with gap" settings.

## Verify
- [ ] Toggle line art off: flats are solid with no gaps or halos.
- [ ] Every character colour matches the colour set.
