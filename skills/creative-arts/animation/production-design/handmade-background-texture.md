---
id: creative-arts.animation.production-design.handmade-background-texture
name: handmade-background-texture
category: creative-arts
field: animation
product: production-design
tags: [production-design, background-painting, bg-texture, traditional-media, scanning, texture]
level: practitioner
status: draft
description: "Give backgrounds a handmade texture: traditional media scans, paper grain, dry brush and watercolour granulation, digital brush capture, and keeping texture scale consistent."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://books.google.com/books?vid=ISBN9780240520933
  - https://animationguild.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handmade texture in backgrounds

Goal: backgrounds that feel painted by hand, whether made on paper or digitally.

## 1. Sources of texture
- **Traditional originals**: gouache, acrylic, watercolour or ink painted on paper, scanned at 600 dpi or
  more in 16-bit to keep subtle tone.
- **Texture library**: scans of paper grain, dry brush strokes, watercolour washes and granulation,
  sponges, pencil. Remove colour casts; store as greyscale with neutral mid-grey.
- **Captured brushes**: turn scanned marks into digital brush tips/grain so painters get consistent marks.

## 2. Applying texture
- Overlay/soft-light texture at a fixed scale relative to the frame (e.g. paper grain visible at 1:1 on
  the delivery resolution). Never scale per BG, or the grain jumps between cuts.
- Vary texture by plane: more visible in the foreground and midground, softer with distance.
- Keep texture out of flat areas behind characters' faces if it fights separation.

## 3. Motion considerations
- Texture locked to the BG plane moves with parallax correctly; screen-locked texture over moving layers
  causes a "shower door" effect. Choose deliberately.

## Verify
- [ ] Texture library scanned and neutralised.
- [ ] Texture scale fixed relative to delivery resolution.
- [ ] Texture tested in a moving shot.

Related: `creative-arts.animation.production-design.background-painting-in-show-style`,
`creative-arts.animation.art-direction.texture-style-targets`.
