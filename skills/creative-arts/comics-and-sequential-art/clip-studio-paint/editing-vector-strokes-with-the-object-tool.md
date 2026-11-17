---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.editing-vector-strokes-with-the-object-tool
name: editing-vector-strokes-with-the-object-tool
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-vector-layer, csp-object-tool, vector-editing, brush-size-change, line-colour]
level: practitioner
status: draft
description: "Edit existing vector strokes with the Object tool in CSP: select lines, change brush size, shape and colour in Tool property, move control points, and recolour line art."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editing vector strokes with the Object tool

## Select
- **Operation** tool > **Object** sub tool. Click a vector line on the active vector layer, or drag a
  rectangle to select several lines; Shift-click adds lines.
- Tool property shows the selected lines' **brush size**, **brush shape**, **main colour**, opacity and
  anti-aliasing.

## What you can change
- **Brush size** - change line width after drawing (whole stroke); width profile from pressure is scaled.
- **Brush shape** - swap a G-pen stroke for a textured or tapered brush shape after the fact.
- **Colour** - recolour line art per stroke (colour holds, red lines for blue-line pencils, coloured
  outlines on webtoon art).
- **Control points** - drag to reshape; delete with Delete key; transform handles move/scale/rotate.
- Delete selected strokes.

## Tips
- Turn on "Select vector lines by clicking" settings in Tool property for precise picking.
- Keep line art on vector layers until the page is final; these edits are impossible after rasterising.
- For colour holds: select lines and set the main colour, keep the layer expression colour as Color.

## Gotchas
- On monochrome or grey expression colour layers, colour changes won't show; set layer to Color.
- Very small selections can grab neighbouring strokes; zoom in.
- Rasterising the layer loses all of this.

## Verify
- [ ] Changed strokes keep their pressure taper and still connect at intersections.
