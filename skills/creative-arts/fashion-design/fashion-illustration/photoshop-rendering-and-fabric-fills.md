---
id: creative-arts.fashion-design.fashion-illustration.photoshop-rendering-and-fabric-fills
name: photoshop-rendering-and-fabric-fills
category: creative-arts
field: fashion-design
product: fashion-illustration
tags: [fashion-design, fashion-illustration, digital-fashion-illustration, digital-illustration, photoshop-rendering, fabric-fill, clipping-mask, adobe-photoshop, fabric-swatch-fill]
level: practitioner
status: draft
description: "Render fashion illustrations in Photoshop: clean line art, flat colour with clipping masks, real fabric fills scaled and warped to the garment, shading with Multiply layers."
sources:
  - https://helpx.adobe.com/photoshop/using/clipping-masks.html
  - https://helpx.adobe.com/photoshop/using/blending-modes.html
  - https://helpx.adobe.com/photoshop/using/warp-images-shapes-paths.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Photoshop rendering and fabric fills

**Goal:** digital renderings with accurate colour and real fabric textures, editable for
colourways.

## Layer setup
1. Line art layer on top, Multiply blend mode (white disappears). Scan at 300-600 dpi or
   draw digitally.
2. Under it, **flat colour** layers per garment piece: select area (Magic Wand on line art
   with "Sample All Layers", expand 1-2 px), fill on its own layer.
3. Lock transparent pixels or use the flat as a **base for clipping masks**.

## Fabric fills
1. Scan or photograph the real swatch flat, in even light, with a colour checker;
   crop to a seamless tile (Filter > Other > Offset to fix seams) and define as a pattern
   (Edit > Define Pattern) or use as a layer.
2. Place above the garment flat, **Alt/Option-click between layers to clip**.
3. Scale to real proportions: estimate pattern repeat size vs garment (a 5 cm check on a
   ~45 cm wide bodice = 9 repeats across).
4. Warp (Edit > Transform > Warp) or use Liquify to follow folds; for large prints use
   Displacement maps.

## Shading
- Shadows layer clipped, Multiply, soft brush in a darker neutral or complementary.
- Highlights layer clipped, Screen or Overlay.
- Keep shading separate from colour so colourways only change the colour/fill layers.

## Colourways
Hue/Saturation or Solid Color adjustment layers clipped per garment; save as layer comps.

## Gotchas
- Fills not scaled to garment size misrepresent prints badly.
- Flattening early prevents colourway changes; keep layered PSD and export copies.
- Screen colour is approximate; reference Pantone codes on the board.

## Verify
- [ ] Line art, colour, fill and shading on separate layers.
- [ ] Print scale checked against real repeat size.
- [ ] Colourway switch possible without repainting.
