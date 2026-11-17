---
id: creative-arts.fashion-design.fashion-illustration.illustrator-brushes-and-flats-library
name: illustrator-brushes-and-flats-library
category: creative-arts
field: fashion-design
product: fashion-illustration
tags: [fashion-design, fashion-illustration, technical-flats, illustrator-brushes, flats-symbol-library, adobe-illustrator, pattern-brush, stitch-brush, cad-flats]
level: practitioner
status: draft
description: "Build an Adobe Illustrator library for flats: stitch pattern brushes, zip and rib brushes, button and trim symbols, swatches and a template file for fast consistent flats."
sources:
  - https://helpx.adobe.com/illustrator/using/brushes.html
  - https://helpx.adobe.com/illustrator/using/symbols.html
  - https://helpx.adobe.com/illustrator/using/libraries.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Illustrator brush and symbol library for flats

**Goal:** draw flats quickly and identically across a team using shared brushes,
symbols and templates.

## Stitch brushes
- Topstitch: a **dashed stroke** works for simple cases (Stroke panel: Dashed Line, e.g.
  dash 2 pt gap 1.5 pt, round caps) - save as a Graphic Style.
- For complex stitches (coverstitch, zigzag, overlock), make a **Pattern Brush**:
  draw one repeat tile, drag into Brushes panel -> New Pattern Brush; set side tile,
  corner tiles (auto-centred), colorization "Tints" so it recolours with stroke colour.
- Name brushes by stitch: `ST_single_2mm`, `ST_twin_6mm`, `ST_cover_406`.

## Other pattern brushes
Zip teeth (coil and metal), rib knit, elastic gathers, piping, braid. Build at the scale
your flats use (keep flats at a fixed croquis size so brushes match).

## Symbols
Buttons (by ligne size), snaps, rivets, eyelets, zip pullers, labels, drawcord ends.
Symbols update all instances when edited (double-click to edit master).

## Template file and libraries
- A `.ait` template with: body template layer (locked), layers for flat outline, stitching,
  details, callouts; artboards for front/back.
- Share brushes, symbols, colour swatches (Pantone TCX approximations) via **Creative
  Cloud Libraries** so the team uses the same assets.

## Gotchas
- Scaling objects with brushes: turn on/off "Scale Strokes and Effects" deliberately;
  pattern brushes scale differently from strokes.
- Expanded brushes can't be edited as brushes; keep live until final export.
- Different croquis sizes across designers break brush scale consistency.

## Verify
- [ ] Brushes and symbols in a shared library with clear names.
- [ ] Template enforces layers and body block.
- [ ] Two designers' flats of the same garment look identical in line weight and stitch.
