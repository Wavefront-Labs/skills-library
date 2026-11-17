---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.lt-conversion-3d-to-line-and-tone
name: lt-conversion-3d-to-line-and-tone
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-3d, csp-lt-conversion, line-extraction, tone-conversion, clip-studio-paint-ex, background-art]
level: advanced
status: draft
description: "Convert 3D or photo layers to line art and tone with CSP EX LT conversion: line extraction width, threshold, tone frequency, posterisation and cleaning up the result."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LT conversion (3D to line and tone)

**Layer > LT conversion of layer** (EX only) turns a 3D layer or an image/photo layer into separate line
and tone layers suitable for monochrome comics.

## Settings
- **Line width** - outline thickness; keep similar to your inking weight at final size.
- **Line extraction** - Contour line (outlines from 3D edges), Inner line (crease/edge detection),
  **Threshold** of edge detection; "Use 3D data contour" gives clean silhouettes on 3D layers.
- **Tone work** - tone on/off; number of tone steps (posterisation levels); **frequency** (lpi) and dot
  type; whether the darkest level becomes solid black.
- **Create texture layer** separates textures from the model.
- Output lines as **vector** where offered so you can edit width afterwards.

## Workflow
1. Set up the 3D background and camera; set light direction for useful shadows.
2. Duplicate the 3D layer (keep the original hidden) and run LT conversion on the copy.
3. Inspect: line layer, tone layer(s), black layer.
4. Clean lines: vector eraser, Correct line tools; delete unnecessary interior lines.
5. Add hand-drawn details and characters on top; adjust tone to match other pages.

## Gotchas
- Default results look mechanical; expect clean-up time.
- Photos give noisy lines; reduce threshold, blur slightly before conversion.
- Frequency mismatch with hand-applied tones causes moire.

## Verify
- [ ] Line weight and tone frequency match surrounding hand-drawn panels at 100% view.
