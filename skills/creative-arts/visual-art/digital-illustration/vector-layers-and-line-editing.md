---
id: creative-arts.visual-art.digital-illustration.vector-layers-and-line-editing
name: vector-layers-and-line-editing
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, digital-inking, digital-line-art, vector-layers, vector-eraser, line-width-correction, control-points, clip-studio-paint, krita-vector]
level: practitioner
status: draft
description: "Ink on vector layers in Clip Studio Paint (and Krita): vector eraser to intersection, Correct line width, control points, Simplify, and when to rasterise."
sources: ["https://docs.krita.org/en/user_manual/vector_graphics.html", "https://www.clipstudio.net/en/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vector layers and line editing

**Goal:** ink lines that remain editable after drawing: thickness, shape and
overlaps, as supported by Clip Studio Paint's vector layers (CSP user guide; Krita
Manual vector graphics).

## Clip Studio Paint vector layers
- New Vector Layer (Layer > New layer > Vector layer). Draw with pens as normal;
  strokes are stored as editable paths with pressure.
- **Vector eraser** (Eraser sub tool, "Vector" option): **Erase up to intersection**
  removes a stroke segment cleanly up to where it crosses another line - perfect
  for tidying overlaps.
- **Correct line width** tool: thicken, thin, or set fixed width on existing strokes.
- **Object** tool: select a stroke and change brush shape, size, colour.
- **Control point** tool: move/add/delete points; **Simplify vector line** reduces
  points; **Redraw vector line** redraws a section.
- Lines scale without loss when transforming the layer.

## Krita vector layers
- Krita's vector layers are SVG-based shapes; good for shapes and paths, less
  suited to pressure-sensitive inking. Most Krita inkers use raster layers with
  stabilisation, or edit in CSP/Inkscape.

## When to rasterise
- Raster effects (textures, smudging, filters) need raster layers. Keep the vector
  ink and duplicate-rasterise when you need a raster version.
- Flatting tools (fill, reference layers) work with vector line art as reference.

## Gotchas
- Vector erasing in "touched area" mode deletes whole strokes unintentionally;
  check the mode.
- Huge stroke counts slow the file; simplify or merge when done.

## Verify
- [ ] Overlaps trimmed with erase-to-intersection.
- [ ] Line weights adjusted with correction tools rather than redrawn.
