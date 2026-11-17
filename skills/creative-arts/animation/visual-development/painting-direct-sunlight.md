---
id: creative-arts.animation.visual-development.painting-direct-sunlight
name: painting-direct-sunlight
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, light-sources, sunlight-painting, direct-sun, warm-light, cast-shadow]
level: practitioner
status: draft
description: "Paint direct sunlight: strong warm key with crisp cast shadows, cool skylight-filled shadows, high light-to-shadow ratio and saturated colour at the terminator."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Sunlight
  - https://en.wikipedia.org/wiki/Color_temperature
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Direct sunlight

Goal: convincing clear-day sunlight - the most common and most demanding light key.

## Characteristics (Gurney)
- **Warm key**: midday sun about 5500K, warm yellow-white; low sun more orange.
- **Cool fill**: shadows lit by the blue sky; outdoors shadows lean blue/violet.
- **High contrast**: light-to-shadow value ratio large; keep a clear gap between the families.
- **Sharp cast shadows** with slight softening far from contact (the sun has about 0.5 degree width).
- **Colour at the terminator**: a narrow band of extra saturation where light turns to
  shadow, especially on skin.
- **Bounce**: strong ground bounce (warm from sand/grass) under forms.

## Method
1. Fix the sun direction and elevation; low sun = long shadows and warm light, high sun = short
   shadows and top-lighting (deep eye sockets, hat shadows).
2. Two-value pass: separate everything into sun and shadow.
3. Paint the light family warm, the shadow family cool and darker by a fixed step.
4. Add reflected light from the ground in shadows, plus occlusion at contacts.
5. Add saturated terminators and sharp highlights.

## Failure modes
- Shadows simply darker versions of the local colour (no sky fill) - looks indoor.
- Too little value gap; the scene looks overcast.
- Inconsistent shadow directions.

## Verify
- [ ] One sun direction across the scene.
- [ ] Warm light / cool shadow relationship.
- [ ] Clear value gap between families.

Related: `creative-arts.animation.visual-development.skylight-fill-and-blue-shadows`,
`creative-arts.animation.blender.sun-light-angle-strength`.
