---
id: creative-arts.animation.vector-graphics.gap-closing-and-paint-bucket-fills
name: gap-closing-and-paint-bucket-fills
category: creative-arts
field: animation
product: vector-graphics
tags: [gap-closing, paint-bucket, ink-and-paint, colour-fills, toon-boom-harmony, line-art]
level: practitioner
status: draft
description: "Colour line art cleanly with gap closing and the paint tool: closing small gaps, when to repair lines instead, paint modes, and checking for unpainted holes."
sources:
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Gap closing and paint bucket fills

Colouring vector line art fills regions bounded by lines. If a line has a gap, the paint leaks out. Gap closing manages this.

## Approaches
1. **Gap-closing options on the fill tool**: the paint/bucket tool in drawing software such as Harmony has options to close gaps of a chosen size (none, small, medium, large) while filling; the tool treats the gap as closed for that fill. Check your software's options.
2. **Close Gap tool**: draws an invisible stroke across a gap so a region is closed permanently (Toon Boom Harmony provides a dedicated Close Gap tool, and the invisible line does not render).
3. **Repair the line**: for gaps that are larger than a few pixels, fix the drawing: extend a line or join it, so the closure is real. This is cleaner if the art goes to other software.

## Paint modes (Harmony)
The paint tool has modes such as Paint (apply to a region), Unpaint, Repaint (only recolour existing colour) and Paint Unpainted (fill only regions with no colour). Repaint is useful when changing a palette colour on a region; check the exact modes in your version.

## Practice
- Use named palette colours, not raw RGB, so colour changes happen in the palette (`harmony-palette-management.md`).
- Fill on a separate colour layer or the "colour art" layer to keep line art separate.
- Zoom in at 200-400% to look for white specks, uncoloured small regions and edge leaks.
- On a scan, vectorise first with controlled threshold (`potrace-vectorisation.md`) to get closed outlines.

## Gotchas
- Gap-closing size is in screen units in some tools: the same gap may close at one zoom and not at another. Close gaps in the art at a fixed zoom or fix them in the line.
- Invisible gap-closing strokes can be lost when drawings are exported to other formats.

## Verify
- [ ] No unpainted regions at 400% zoom across the shot.
- [ ] Palette colour change updates all regions.
