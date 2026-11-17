---
id: creative-arts.animation.visual-development.artificial-light-and-luminescence
name: artificial-light-and-luminescence
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, light-sources, luminescence, neon, artificial-light, glow]
level: practitioner
status: draft
description: "Paint artificial light and luminescence: neon, screens, streetlights and bioluminescence - colour, falloff, glow halos and keeping self-lit objects readable."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Neon_lighting
  - https://en.wikipedia.org/wiki/Bioluminescence
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Artificial light, neon and luminescence

Goal: believable glowing sources - signs, screens, lamps, magic, bioluminescent creatures.

## Source types (Gurney)
- **Incandescent/tungsten**: warm (2700-3200K), point source, sharp shadows.
- **Fluorescent / LED**: cool or green-tinted to neutral; often long tubes - soft directional.
- **Sodium vapour streetlights**: monochromatic orange; colours under it collapse to orange and black.
- **Neon**: saturated line sources; colour spills onto nearby surfaces and wet ground.
- **Screens**: cool, flickering, lighting faces from the front/below.
- **Luminescence** (fireflies, deep-sea creatures, magic): self-lit objects with a small light radius.

## Painting glow
1. Keep the surroundings dark enough; glow only reads by contrast.
2. Paint the source near white at its core with saturated colour around it (the core
   desaturates as it overexposes).
3. Add a soft halo (bloom) proportional to atmosphere; more haze = bigger halo.
4. Spill the colour onto nearby surfaces with falloff; shadows from the glow face away from it.
5. Use colour contrast: warm glow against cool night, or complementary neon pairs.

## Failure modes
- Glowing object that lights nothing around it - reads as flat paint.
- Saturated colour at the hottest core (should go toward white).
- Too many coloured sources fighting; no hierarchy.

## Verify
- [ ] Each source spills onto its surroundings.
- [ ] Core lighter and less saturated than the halo.
- [ ] One dominant source per area.

Related: `creative-arts.animation.visual-development.color-accents`,
`creative-arts.animation.blender.light-nodes-falloff`.
