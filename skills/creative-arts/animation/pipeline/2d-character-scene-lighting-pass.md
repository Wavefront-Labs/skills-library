---
id: creative-arts.animation.pipeline.2d-character-scene-lighting-pass
name: 2d-character-scene-lighting-pass
category: creative-arts
field: animation
product: pipeline
tags: [compositing, 2d, cel, two-tone, terminator, rim-light, scene-lighting, character-lighting, key-shade, numpy, pillow, anime, daima, puppet, colour, integration]
level: practitioner
status: verified
description: "Integrate a flat-lit 2D character into a painted scene: cel two-tone key/shade with a hard diagonal terminator across the character's own width, a rim on the lit edge, then a contrast lift."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# 2D character scene-lighting pass

A character drawn on a white background is evenly lit; drop it onto a painted
scene with raking sun and it floats. Anime fixes this with a cel shadow, not a
gradient. Verified in three iterations beside Dragon Ball Daima close-ups.

## Do this (per frame, on the composited character RGBA layer, before the plate)
1. **Measure the character's own width** from its alpha (first and last columns with
   alpha > 0.05). All geometry below is 0..1 across THAT width, never across the
   frame — a frame-relative gradient put the terminator through the middle of the
   face when the character was centred.
2. **Two-tone tint**: key colour from the scene's light (warm sun: `(255,214,160)`),
   shade colour from its fill (`(150,128,170)` for a cool sky). Terminator at
   `x = 0.22 + 0.10·y` (slightly diagonal), softened over 5 % of the width. Blend:
   `rgb × (0.70 + 0.30 × tint) × 1.06` — multiply, lifted so midtones survive.
3. **Rim light**: erode the alpha by 9 px, subtract from the original alpha, keep only
   the lit side, add `key × 0.9` along that band.
4. Composite over the plate, then **contrast 1.12** on the whole frame.

## Numbers that failed first
- Terminator at 0.40 with a dark shade `(96,84,128)` put half the face in shadow: a
  dark mask. Shade must be a band on the far side (≤ 25 % of the width) and lighter
  than you think; the hard edge does the work, not the darkness.
- A smooth left-to-right gradient reads as a Photoshop filter. Anime is two tones
  with one hard edge.

## Palette match
If the character's local colours are duller than the scene (a traced grey-mauve
hair against a warm painted alley), recolour the fills once at the source: hue to the
scene's warm family, saturation ×1.9 + 0.18, value ×0.92. Do it on the vector paths
so every frame inherits it — see
`creative-arts.animation.vector-graphics.parametric-features-over-traced-master`.

## Verify
A/B the frame with the pass toggled: with it, the character sits on the same plane
as the scene light (lit side matches the sunlit wall, shade side matches the shadowed
wall); the rim traces the silhouette on the sun side only; no face region is darker
than the scene's own shadows.

## Light each character separately
Lighting the merged character layer puts the terminator at a fraction of the LAYER's
bounding box: in a two-shot the left figure fell wholly on the shade side and read as a
grey ghost. Light each figure's own layer, then composite.
