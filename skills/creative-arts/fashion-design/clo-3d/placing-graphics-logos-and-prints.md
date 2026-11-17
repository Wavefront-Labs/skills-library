---
id: creative-arts.fashion-design.clo-3d.placing-graphics-logos-and-prints
name: placing-graphics-logos-and-prints
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-texture, clo-graphic, clo-print-placement, logo-placement, artwork-placement, graphic-property]
level: practitioner
status: draft
description: "Place graphics, logos and placement prints in CLO 3D: graphic tool, sizing to real dimensions, positioning from landmarks, transparency, displacement and print types."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Placing graphics, logos and prints in CLO

**Goal:** artwork placed at its real size and position, as the factory will print or
embroider it, visible in 3D and on the tech pack.

## Adding graphics
1. Use the **Graphic** tool (Add Graphic) in the 2D window; choose the image (PNG with
   transparency, JPG, or vector-derived high-res image).
2. Click on the pattern to place; the graphic appears as an object in Object Browser >
   Graphic.
3. Use **Transform Graphic** to move, rotate and scale; type exact width/height in mm in the
   Property Editor.

## Positioning
- Measure from landmarks as in the tech pack: "8 cm below HPS, centred on CF".
- Use 2D rulers and the measurement tool; centre on symmetric patterns.
- Graphics crossing seams: place separately on each pattern and align, or use print across
  a sewn layout where supported.

## Properties
- Texture image, colour, transparency, **normal/displacement** for embroidery and
  puff-print relief, roughness/metalness for foil.
- Graphic type presets (print, embroidery, patch) where available.
- Order of graphics when overlapping.

## Fabric texture vs graphic
- **All-over prints** belong in the fabric's texture (repeat), not as graphics.
- **Placement prints, logos, labels, patches** are graphics.

## Gotchas
- Low-resolution artwork blurs in close-up renders; use 300 dpi at real size.
- Scaling by eye instead of mm misrepresents print size.
- Graphics on stretchy areas distort in 3D like real prints; check on the avatar.

## Verify
- [ ] Graphic size in mm matches the artwork spec.
- [ ] Position measured from landmarks.
- [ ] Embroidery/puff effects use normal or displacement maps.
