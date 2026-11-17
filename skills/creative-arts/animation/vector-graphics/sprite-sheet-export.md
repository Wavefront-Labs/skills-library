---
id: creative-arts.animation.vector-graphics.sprite-sheet-export
name: sprite-sheet-export
category: creative-arts
field: animation
product: vector-graphics
tags: [sprite-sheet, vector-export, svg-export, sprite-atlas, adobe-animate, texturepacker, imagemagick-montage, game-animation, json-atlas]
level: practitioner
status: draft
description: "Export 2D animation as sprite sheets with data files for games and web: Animate's Generate Sprite Sheet, TexturePacker-style packing, ImageMagick montage, padding and trimming."
sources:
  - https://helpx.adobe.com/animate/using/create-sprite-sheet.html
  - https://imagemagick.org/script/montage.php
  - https://www.codeandweb.com/texturepacker/documentation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sprite sheet export

**Goal:** an animation as one image (or a few) plus frame data, loadable by a game engine or web player with
correct frame order, pivots and no bleeding between frames.

## Adobe Animate

Select a symbol in the library or on stage - right-click **Generate Sprite Sheet**: choose frames, algorithm
(Basic or MaxRects), data format (JSON, JSON-Array, Starling, cocos2D, EaselJS...), border/shape padding, trim,
image format PNG 32-bit. Export writes `sheet.png` + `sheet.json`.

## From a rendered PNG sequence

ImageMagick grid (uniform cells, simple players):
```bash
magick montage run_*.png -tile 8x -geometry +0+0 -background none run_sheet.png
```
Cells are uniform at the largest frame size; frame N is at column N%8, row N/8.

Packed atlas with trimming (smaller, needs data): TexturePacker CLI:
```bash
TexturePacker --format json-array --data run.json --sheet run.png --trim-mode Trim \
  --extrude 1 --shape-padding 2 --border-padding 2 --max-size 4096 run_*.png
```
Trimmed frames store their original size and offset in the JSON so pivots stay correct.

## Settings that matter

- **Padding/extrude** 1-2 px prevents neighbouring frames bleeding with bilinear filtering and mipmaps.
- **Power-of-two** sheet sizes for older engines/WebGL1.
- **Premultiplied alpha** matching the engine's expectation.
- Max sheet size per target (4096 on most desktop/mobile, 2048 for old devices).

## Gotchas

- Frame sorting: unpadded numbers (`run_10` before `run_2`) scramble animation; pad frame numbers.
- Trimming changes frame sizes; engines must use the JSON's source size/offset or characters jitter.
- Vector line art rasterised small aliases; render at target size, not scaled down in the engine.

## Verify

Load the sheet in the target engine or a test HTML player: animation plays in order at the right speed with no
jitter, no edge bleeding at frame borders when scaled.
