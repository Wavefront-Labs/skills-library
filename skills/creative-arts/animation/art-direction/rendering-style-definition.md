---
id: creative-arts.animation.art-direction.rendering-style-definition
name: rendering-style-definition
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, art-bible, rendering-style, brush-language, npr, edges]
level: advanced
status: draft
description: "Define a show's rendering and brush language: shading steps, edge treatment, brush and texture sources, highlight shapes and line, with CG equivalents."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://www.gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The
  - https://en.wikipedia.org/wiki/Non-photorealistic_rendering
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rendering style and brush language

Goal: every artist and every shader renders surfaces the same way, so the frame reads as one hand.

## 1. Decide the shading model
- Number of tones: flat (1), cel (2: light + shadow), cel + highlight (3), painterly (continuous).
- Shadow edge: hard, soft, or hard with a narrow soft band at the terminator.
- Where gradients are allowed (sky only? never on characters?).
- Highlight shapes: geometric (rectangles, crescents) or organic; size relative to the form.

## 2. Brush language (2D and painted textures)
- Named brush set shipped with the bible (files and settings), with a sample stroke sheet.
- Stroke direction rule: follow form, or a fixed diagonal hatch for unity.
- Texture source: paper grain, gouache dry brush, scanned media; grain size at delivery resolution.
- Edge vocabulary: hard on focal silhouettes, lost edges inside shadow masses.

## 3. Line treatment
- Outline yes or no; weight varied by depth or by light; inner vs silhouette lines; line colour.

## 4. CG translation
- State the shader equivalent of each rule: toon ramp steps, shadow colour, rim width, outline method
  (inverted hull vs post-process), texture projection. Arc System Works' Guilty Gear Xrd GDC talk is the
  standard reference for 2D-matched CG (hand-edited normals, per-vertex shadow thresholds).

## Verify
- [ ] Shading tone count, edge and highlight rules written with examples.
- [ ] Brush set and stroke sheet delivered.
- [ ] CG equivalents listed for each rule.

Related: `creative-arts.animation.art-direction.painting-to-shader-targets`,
`creative-arts.animation.art-direction.npr-look-targets`,
`creative-arts.animation.texturing.texture-painting`.
