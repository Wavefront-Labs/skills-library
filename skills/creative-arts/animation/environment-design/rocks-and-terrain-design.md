---
id: creative-arts.animation.environment-design.rocks-and-terrain-design
name: rocks-and-terrain-design
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, natural-environment, terrain-design, rocks, landforms, geology]
level: practitioner
status: draft
description: "Design rocks and terrain: plane-based rock forms, geology-driven fracture patterns, terrain layering and scale variety for believable stylized landscapes."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://books.google.com/books?vid=ISBN9780740785504
  - https://en.wikipedia.org/wiki/Landform
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rocks and terrain

Goal: rocks and landscapes that look solid, geologically plausible and designed.

## Rocks
- **Planes**: rocks read as sets of flat planes - top plane (lightest, gets sky), side planes
  (mid), underside (darkest). Design with angular planes, then round edges per style.
- **Geology**: sedimentary = horizontal layers and blocky breaks; granite = rounded boulders and
  vertical cracks; volcanic = jagged, porous; slate = thin sheets. Pick one per location.
- **Size variety**: big-medium-small clusters, with small rocks gathering at the base of big ones
  (scree) and settling into the ground (not sitting on it).
- **Cracks follow structure**: consistent direction within a rock type.

## Terrain
- Layer the landscape into overlapping ridges that step back in value (atmospheric perspective).
- Water flow shapes land: valleys V-shaped from rivers, U-shaped from glaciers; erosion
  lines run downhill.
- Grounding: plants and debris collect in hollows and at the base of slopes.
- Silhouette rhythm: vary ridge heights and angles; avoid parallel lines between ridges.

## Method
1. Choose geology and climate for the location.
2. Block big landforms as value shapes; establish horizon and ridges.
3. Add rocks as plane groups with the chosen fracture pattern.
4. Embed and ground them with grass, debris, contact shadows.
5. Test readability in greyscale.

## Failure modes
- Blob rocks without planes (potatoes).
- Mixed geology in one shot without reason.
- Rocks floating on the ground with no occlusion contact.

## Verify
- [ ] Top/side/bottom plane values consistent with light.
- [ ] Fracture pattern matches geology.
- [ ] Rocks embedded with contact shadows.

Related: `creative-arts.animation.visual-development.occlusion-shadows`,
`creative-arts.animation.environment-design.depth-planes`.
