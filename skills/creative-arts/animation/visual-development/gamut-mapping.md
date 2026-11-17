---
id: creative-arts.animation.visual-development.gamut-mapping
name: gamut-mapping
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, color-theory, gamut-mapping, limited-palette, color-harmony, gurney]
level: advanced
status: draft
description: "Plan a palette with Gurney's gamut mapping: draw a shape on the colour wheel, mix only colours inside it, and pick shapes for the mood of each scene."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Gamut
  - https://gurneyjourney.blogspot.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gamut mapping

Goal: a unified, intentional palette by restricting colours to a chosen region of the colour
wheel (Gurney's gamut masking).

## How it works
- On a colour wheel with grey at the centre and full saturation at the rim, draw a polygon
  (the mask). Only colours inside it are allowed.
- The polygon's vertices are the most saturated colours available; the centre of the shape
  is the image's neutral.
- Colours outside the mask are unavailable, so even "grey" reads relative to the gamut and
  the image feels lit by one light.

## Common shapes
- **Triangle (triad)**: three primaries of the scene; good for balanced but restrained images.
- **Atmospheric triangle off-centre**: mostly one hue family plus a small complementary tip - mood keys.
- **Narrow ellipse along a complementary axis**: warm/cool contrast (orange-blue night/day).
- **Small shape near the centre**: muted, foggy, melancholic.
- **Shape that excludes a hue**: e.g. no greens at all for an alien world.

## Method
1. Draw the colour wheel (or use a gamut mask tool: Krita, Procreate add-ons, online gamut
   mask tools).
2. Draw the mask for the scene's mood; write the 3-5 vertex colours down.
3. Pre-mix a palette from those vertices only (digital: make swatches from the mask).
4. Paint using only the swatches and mixtures between them.
5. Do a variant mask per sequence for the colour script.

## Failure modes
- Mask drawn but pure out-of-gamut accents sneak in.
- Shape too large: no unity gained.
- Same mask for every scene: the film has no colour arc.

## Verify
- [ ] Every colour lies inside the mask.
- [ ] Mask shape chosen for the scene mood.
- [ ] Masks per sequence vary along the colour script.

Related: `creative-arts.animation.visual-development.color-harmony-schemes`,
`creative-arts.animation.art-direction.color-script`.
