---
id: creative-arts.animation.visual-development.subsurface-and-translucency-in-paint
name: subsurface-and-translucency-in-paint
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, light-properties, subsurface-painting, subsurface-scattering, skin-painting, translucency]
level: advanced
status: draft
description: "Paint subsurface scattering and translucency: warm saturated terminators on skin, glowing thin parts in backlight, and softened shadows on wax, leaves and flesh."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Subsurface_scattering
  - https://books.google.com/books?vid=ISBN9781933492964
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subsurface scattering and translucency in paint

Goal: materials that let light in - skin, wax, marble, leaves, grapes, ears - painted so they
look fleshy and alive rather than plastic.

## Observable effects (Gurney)
- **Warm terminator**: light enters the lit side, scatters and exits near the terminator
  with a saturated warm (red-orange for skin) band.
- **Soft shadows**: the shadow edge on translucent materials is softer than on opaque ones.
- **Thin-part glow**: ears, nostrils, fingers, leaves glow when backlit; the glow takes the
  material's inner colour (red for flesh, yellow-green for leaves).
- **Lower contrast** between light and shadow because light leaks across.

## Method
1. Paint the form as opaque first.
2. Soften the terminator edge and add a narrow saturated warm band along it.
3. Lift the shadow slightly with the material's inner colour near the terminator.
4. For backlit thin parts, paint a glow with the inner colour and a slightly lighter value
   than the surrounding shadow.
5. Keep highlights on top (specular is a surface effect, unaffected by SSS).
6. In CG use an SSS shader with a radius matched to scale; in NPR, a warm ramp step at the
   terminator imitates it.

## Failure modes
- Grey or muddy terminators on skin (dead look).
- Overdone glow making characters look like wax.
- SSS radius too large for the character's scale in CG.

## Verify
- [ ] Warm band at skin terminators.
- [ ] Thin parts glow when backlit.
- [ ] Highlights still sit on the surface.

Related: `creative-arts.animation.visual-development.rim-light-and-backlight`,
`creative-arts.animation.environment-design.trees-and-foliage-stylization`.
