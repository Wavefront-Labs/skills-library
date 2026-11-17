---
id: creative-arts.animation.art-direction.texture-style-targets
name: texture-style-targets
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, look-development, texture-style, texture-painting, surfacing]
level: practitioner
status: draft
description: "Set texture-painting style targets: hand-painted vs procedural, scale of detail, wear language, colour variation limits and a calibration sheet surfacing artists match."
sources:
  - https://www.khanacademy.org/computing/pixar
  - https://animationguild.org/
  - https://books.google.com/books?vid=ISBN9780740785504
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Texture painting style targets

Goal: every asset's textures look made by one studio at one scale.

## 1. Choose the texture language
- Hand-painted (light and shadow partly in the albedo), stylised PBR (clean albedo, painted variation),
  or realistic PBR. State which; mixing breaks the look.
- Detail scale: smallest painted feature in screen pixels at the typical shot size (e.g. no detail
  smaller than 4 px at a medium shot). Texture density (texels/metre) fixed per asset class.

## 2. Wear and variation language
- Where wear goes (edges, contact points, high-traffic areas), how it is shaped (chunky stylised chips vs
  realistic scratches), and maximum coverage.
- Colour variation: hue/value jitter limits (e.g. plus or minus 5% value) so surfaces live but stay graphic.

## 3. Calibration sheet
- A sphere, cube and a typical prop textured in the target style, rendered under the standard lookdev
  light rig, plus a material swatch chart (wood, metal, fabric, skin, stone).
- Every new asset is reviewed beside the calibration sheet in the same rig.

## 4. Delivery rules
- Map set and naming, colour space per map (albedo sRGB; roughness/normal raw), resolution per class.

## Verify
- [ ] Texture language and detail scale written.
- [ ] Wear rules and variation limits defined.
- [ ] Calibration sheet exists and is used in review.

Related: `creative-arts.animation.texturing.texture-painting`,
`creative-arts.animation.texturing.textures-maps`,
`creative-arts.animation.art-direction.lookdev-turntables`.
