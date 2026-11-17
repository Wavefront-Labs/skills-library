---
id: creative-arts.animation.environment-design.aerial-perspective-shift
name: aerial-perspective-shift
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, atmospheric-perspective, aerial-perspective, value-shift, color-shift, haze, distance, background-painting, gurney]
level: practitioner
status: draft
description: "Paint aerial perspective: how values, contrast, saturation and hue shift toward the atmosphere color with distance, by time of day and weather, per Gurney."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Aerial_perspective
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aerial perspective shift

Goal: distant objects look distant because the air between them and the viewer changes their
color and value - Gurney's Color and Light covers the mechanics.

## What changes with distance
1. **Value**: darks lighten (dark mountains become pale); lights may darken slightly toward the
   air color.
2. **Contrast**: decreases - the value range compresses.
3. **Saturation**: decreases.
4. **Hue**: shifts toward the color of the atmosphere - blue in clear daylight (Rayleigh
   scattering), warm orange/yellow at sunset or in dust, grey in overcast, near-white in fog.
5. **Edges and detail**: soften and disappear.

## Method
1. Decide the atmosphere color for the shot (time of day and weather).
2. For each depth plane, mix its local colors toward that atmosphere color; more for farther planes.
3. Compress value range per plane.
4. In digital painting, use a layer of the atmosphere color with opacity increasing by distance
   (or a depth-pass fog in 3D) - then hand-adjust.
5. Exception: backlit scenes against a bright sky can make distant silhouettes darker than mid-distance.

## Failure modes
- Distant elements as saturated and contrasty as foreground - looks pasted on.
- Blue haze in a sunset scene (atmosphere color mismatched).
- Uniform fog that kills the focal point.

## Verify
- [ ] Value range and saturation decrease with distance.
- [ ] Distant hues shift toward the chosen atmosphere color.
- [ ] Focal point still holds strongest contrast.

Related: `creative-arts.animation.environment-design.depth-planes`,
`creative-arts.animation.production-design.background-painting`.
