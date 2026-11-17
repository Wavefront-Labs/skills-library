---
id: creative-arts.animation.visual-development.reflected-light-and-bounce-color
name: reflected-light-and-bounce-color
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, light-properties, reflected-light, bounce-light, color-bleeding, shadow-color]
level: practitioner
status: draft
description: "Paint reflected light and bounce colour: secondary light from lit surfaces tinting nearby shadows, its strength by distance and surface, kept within shadow values."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Global_illumination
  - https://books.google.com/books?vid=ISBN9781933492964
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reflected light and bounce colour

Goal: shadows that are alive with the colour of surrounding lit surfaces, without
breaking the form.

## Rules (Gurney)
- Any lit surface becomes a secondary source. A red wall in sun bounces red into the
  shadow side of a figure beside it; green grass bounces green under a chin.
- **Strength** depends on how bright and how close the bouncing surface is and how much of it
  the receiving surface faces.
- **Colour** is the bouncing surface's local colour multiplied by the key light colour.
- **Value**: reflected light stays in the shadow family - always darker than the halftones
  in the light.
- Strongest on shadow planes facing the bouncing surface; absent in crevices (occlusion).

## Method
1. List the big lit surfaces near the subject (ground, walls, large props).
2. For each shadow plane, ask which of those it faces.
3. Tint those shadow planes toward the bounce colour; strongest near the bouncing surface.
4. Compare against the halftones; pull down any reflected light that competes.
5. In CG this is global illumination; in cel/NPR looks, add it as a rim-like colour
   shift in the shadow tone or a separate light.

## Failure modes
- Reflected light so bright the shadow loses unity (double-lit look).
- Bounce colour unrelated to the environment (arbitrary purple).
- Bounce added everywhere, including crevices.

## Verify
- [ ] Each bounce has a visible source surface.
- [ ] Reflected light darker than lit halftones.
- [ ] Crevices remain dark.

Related: `creative-arts.animation.visual-development.light-halftone-core-shadow`,
`creative-arts.animation.blender.cycles-light-bounces`.
