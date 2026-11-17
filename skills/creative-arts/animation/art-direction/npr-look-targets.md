---
id: creative-arts.animation.art-direction.npr-look-targets
name: npr-look-targets
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, look-development, npr-look, stylized-rendering, cel-shading, look-target]
level: advanced
status: draft
description: "Define non-photoreal look targets for CG: reference frames, line, shading steps, texture and frame-rate choices, and a test shot that proves the look before production."
sources:
  - https://www.gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The
  - https://www.khanacademy.org/computing/pixar
  - https://en.wikipedia.org/wiki/Non-photorealistic_rendering
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Non-photoreal look targets

Goal: a stylised CG look specified well enough that lookdev can hit it and the director can approve it on a
real shot.

## 1. Paint the target
- 3-5 **target frames** painted over blocked-in renders of real story moments (one close-up, one wide,
  one night, one action).
- Annotate each with what is rendering vs paint vs comp: outlines, shadow shape, texture, halftone,
  colour fields.

## 2. Decide the levers
| Lever | Options |
|---|---|
| Shading | toon ramp steps, hand-placed shadow shapes, painterly strokes |
| Line | inverted hull, post-process edge detection, hand-drawn line layers |
| Texture | screen-space vs object-space (object-space avoids the "shower door" effect) |
| Frame rate | on 1s, on 2s, or mixed per character (Spider-Verse-style) |
| Normals | edited/transferred normals for clean face shading |
| Comp | halftones, chromatic offsets, painted overlays |

## 3. Prove it on a test shot
- Pick a hard shot (moving camera, close-up face, lighting change). The look must hold in motion,
  at delivery resolution, under the show's lighting states.
- Measure cost: render time and artist time per shot; a look that needs per-frame paint fixes must be
  budgeted that way.

## 4. Lock
- The approved test shot plus target frames become the look reference in the bible.

## Verify
- [ ] Target frames painted over real shots, annotated by technique.
- [ ] Test shot in motion approved.
- [ ] Per-shot cost known.

Related: `creative-arts.animation.art-direction.painting-to-shader-targets`,
`creative-arts.animation.art-direction.rendering-style-definition`,
`creative-arts.animation.art-direction.look-development`.
