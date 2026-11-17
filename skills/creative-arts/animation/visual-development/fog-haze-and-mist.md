---
id: creative-arts.animation.visual-development.fog-haze-and-mist
name: fog-haze-and-mist
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, atmospheric-effects, fog-haze, mist, atmospheric-perspective, depth]
level: practitioner
status: draft
description: "Paint fog, haze and mist: values and colours converge on the fog colour with distance, edges soften, lights bloom, and density sets how fast detail disappears."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Fog
  - https://en.wikipedia.org/wiki/Haze
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fog, haze and mist

Goal: atmosphere that creates depth and mood by veiling distance.

## Behaviour (Gurney)
- Every object fades toward the **fog colour** (its value and hue) as distance increases.
  Darks lighten fastest; lights may darken slightly toward the fog value.
- **Density** controls the rate: thin haze shifts over kilometres; thick fog swallows objects
  in metres - big near/far contrast in a short space.
- **Edges** soften and detail drops with distance.
- **Light sources bloom**: halos around lamps and the sun; shafts appear when light is blocked
  (see god rays).
- **Ground fog** sits in low areas, layered and lighter at the bottom; tops of objects poke out.
- Haze colour: blue on clear days, warm at sunset, grey-white in fog, brown/yellow in smog or dust.

## Method
1. Choose fog colour and density from the story and time of day.
2. Paint each depth plane closer to the fog colour as it recedes - a fixed step per plane.
3. Lose edges and detail progressively.
4. Add halos around lights; add shafts if a strong source is partly blocked.
5. Keep silhouettes of key shapes readable even when faint.
6. In CG: volume scatter or a Z-depth mist pass mixed in comp; match density across shots.

## Failure modes
- Uniform grey overlay with no distance gradient.
- Near objects fogged as much as far ones.
- Fog that hides the story element.

## Verify
- [ ] Values step toward the fog colour with distance.
- [ ] Edges soften with distance.
- [ ] Key silhouettes still read.

Related: `creative-arts.animation.environment-design.aerial-perspective-shift`,
`creative-arts.animation.blender.volumetrics-atmospherics`.
