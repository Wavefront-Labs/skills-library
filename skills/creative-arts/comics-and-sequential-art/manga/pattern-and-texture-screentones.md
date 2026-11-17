---
id: creative-arts.comics-and-sequential-art.manga.pattern-and-texture-screentones
name: pattern-and-texture-screentones
category: creative-arts
field: comics-and-sequential-art
product: manga
tags: [manga, screentone, manga-tones, pattern-tone, texture-tone, sand-tone, background-tones]
level: practitioner
status: draft
description: "Use pattern and texture screentones in manga: sand, noise, line, flower and fabric patterns, choosing scale for reduction, layering over gradation tones and avoiding moire."
sources:
  - https://deleter-mangashop.com/en/
  - https://en.wikipedia.org/wiki/Screentone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pattern and texture screentones

Beyond flat dot tones, manga uses pattern and texture tones for materials, moods and backgrounds.

## Common types
| Tone | Use |
|---|---|
| Sand / noise (suna) | grain, ageing, gritty atmosphere, night skies |
| Line tones (parallel, concentric) | speed, rain, glass, mood backgrounds |
| Cross-hatch tone | shading without drawing hatching, a retro look |
| Flower / sparkle / bubble backgrounds | shojo emotional backgrounds (*sehai*) |
| Fabric (plaid, check, polka dot) | clothing patterns |
| Wood, stone, brick, concrete | backgrounds and props |
| Effect tones (lightning, smoke) | ready-made effects |

## Applying
1. Choose a scale that survives reduction: fine textures at B4 printed at 80% may plug up.
2. Cut along the contours; overlap slightly under black lines.
3. Rotate line and fabric patterns to follow form (stripes curve with a sleeve; for traditional tone,
   deform by cutting and repositioning pieces).
4. Combine: pattern over a light dot tone for depth; sand over gradation for gritty shading.

## Digital (CSP)
- Material palette > Monochromatic pattern / Texture: drag onto a selection to create a tone layer.
- Use Mesh transformation to wrap patterns on clothing.
- Set the output to monochrome 2-tone and check at 100% view; pattern tones are bitmaps so they must not
  be scaled after placement (re-place instead).

## Gotchas
- Two dot-based tones at different angles stacked = moire; stack only patterns with compatible lpi/angle
  or use a non-dot texture.
- Busy patterns behind dialogue reduce legibility; mask out behind balloons.

## Verify
- [ ] Print a test at final reduction; patterns read and do not form moire.
