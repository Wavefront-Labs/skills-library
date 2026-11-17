---
id: creative-arts.animation.production-design.background-reuse-library
name: background-reuse-library
category: creative-arts
field: animation
product: production-design
tags: [production-design, background-painting, bg-reuse, asset-library, tv-production]
level: practitioner
status: draft
description: "Plan background reuse for series production: stock BGs, cropped and flipped variants, layered BGs for redressing, naming, and a searchable library."
sources:
  - https://animationguild.org/
  - https://help.autodesk.com/view/SGSUB/ENU/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Background reuse and library

Goal: save painting time by reusing backgrounds without the audience feeling repetition.

## 1. Plan reuse from the start
- Identify **stock locations** (the house, the school hallway) used every episode; paint them as
  high-resolution masters wider and taller than any shot needs, with layers per plane and dressing.
- Paint lighting states (day, night) as separate versions or adjustment layers.

## 2. Ways to reuse
- Crop and reframe a master for different shot sizes; pan within a wide master.
- Flip horizontally only where there is no text, asymmetric landmark or established geography.
- Redress via layers: swap props, signage, season details.
- Recolour for lighting states using the palette variants.

## 3. Library
- Name: `loc_kitchen_master_day_v003`, crops `..._crop_ms_01`.
- Metadata: location, angle, lighting state, episode first used, dressing variant, resolution.
- Thumbnail browser; layout artists search the library before requesting a new BG.

## 4. Avoid visible repetition
- Do not reuse a distinctive BG twice in the same sequence from the same angle without change.
- Rotate dressing variants and vary crops.

## Verify
- [ ] Stock locations painted as layered oversize masters.
- [ ] Library tagged and searchable.
- [ ] Flips checked for text and geography.

Related: `creative-arts.animation.pipeline.asset-management`,
`creative-arts.animation.production-design.background-painting-in-show-style`.
