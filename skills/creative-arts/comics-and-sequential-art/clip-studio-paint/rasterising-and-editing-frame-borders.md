---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.rasterising-and-editing-frame-borders
name: rasterising-and-editing-frame-borders
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-frame-border, csp-frame-rasterize, frame-border-folder, panel-border-style, hand-drawn-border]
level: practitioner
status: draft
description: "Edit and rasterise CSP frame borders: change width and colour with the Object tool, convert frame folders to raster for hand-drawn borders, broken and irregular panels."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rasterising and editing frame borders

## Editing while still a frame border
- Select the frame folder's border with the **Object** tool: Tool property shows **Brush size** (border
  width), **brush shape** (rough brush shapes give a hand-drawn look), and colour.
- Move corners or edges by dragging control points; Shift constrains.
- **Cut frame border** tool splits a panel; gutters follow settings in Tool property.
- Turn off the border on one panel to make a borderless panel (Tool property > Draw border/Display
  border unchecked).

## Rasterise
- With the frame border folder selected: **Layer > Rasterize**. The border becomes a raster layer and the
  panel mask stays as a layer mask on the folder (exact result varies with version; check the layers
  palette).
- Now draw on the border by hand: wobbly lines, broken corners, ink splatter, or erase segments so
  characters break out.
- Alternative without rasterising: draw over the border on a new layer above and hide the original border.

## When to rasterise
- Hand-drawn style borders, irregular textures or partial borders.
- Keep a copy of the page (or duplicate the folder hidden) because you lose editable frame geometry.

## Gotchas
- Rasterised borders don't adjust when you resize the panel; finish layout first.
- Rasterising at low resolution on a colour page gives soft borders; check page resolution (600 dpi
  monochrome, 350 colour).

## Verify
- [ ] Border width consistent across the page at 100% zoom.
- [ ] Mask still clips panel art after rasterising.
