---
id: creative-arts.design-for-form-and-experience.concept-design.knitting-trimming-and-thickening-surfaces-to-a-solid
name: knitting-trimming-and-thickening-surfaces-to-a-solid
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [knit-surface, thicken-surface, trim-surface, surface-to-solid, solidworks-surfacing, surfacing]
level: practitioner
status: draft
description: "Turn surface bodies into a solid in SOLIDWORKS: trim, knit with gap control, create a solid from a closed volume, or thicken an open surface, and fix failures."
sources:
  - "SOLIDWORKS Help (help.solidworks.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Knit, trim and thicken to a solid

Goal: finish a surface model as a manufacturable solid.

## Steps
1. **Trim** (Insert > Surface > Trim): trim two intersecting surfaces mutually or cut with a surface or sketch; confirm trimmed edges meet cleanly.
2. **Knit** (Insert > Surface > Knit): select all surface bodies. Tick **Create solid** when the surfaces fully enclose a volume. **Merge entities** merges coincident faces where appropriate. **Gap control** shows gaps within the tolerance that will be closed.
3. **Thicken** (Insert > Boss/Base > Thicken) to give an open surface thickness: choose side 1, side 2 or mid-surface and set the value. The **Create solid from enclosed volume** option applies when the knitted surface encloses a volume.
4. Add draft, ribs, fillets and shell on the resulting solid.

## Failures and fixes
- Knit leaves open edges: use the gap information in the Knit PropertyManager; extend or trim surfaces so edges coincide; close holes with Delete Face (patch) or Filled Surface.
- Thicken fails on tight curvature: thickness exceeds the minimum radius of curvature; reduce the thickness or relax the surface.
- Sliver faces: remove them with Delete Face or rebuild the offending patch.

## Verify
- [ ] The tree lists a Solid Body, not Surface Bodies.
- [ ] Mass properties evaluate on the solid.
- [ ] Zebra and curvature stay smooth after thickening.
