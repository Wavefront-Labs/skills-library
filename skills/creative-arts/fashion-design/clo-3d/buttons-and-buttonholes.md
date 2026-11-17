---
id: creative-arts.fashion-design.clo-3d.buttons-and-buttonholes
name: buttons-and-buttonholes
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-trims, 3d-trims, clo-buttons, clo-buttonhole, fasten-button, button-library]
level: practitioner
status: draft
description: "Add buttons and buttonholes in CLO 3D: placing buttons and holes, button properties and library, fastening buttons to holes, and spacing them evenly on plackets."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Buttons and buttonholes in CLO

**Goal:** realistic buttons placed and fastened through buttonholes so plackets close as in
a real garment.

## Placing
1. **Button** tool: click on the 2D pattern (or 3D) where buttons go. Right-click a placed
   button > copy/move with exact spacing, or use the option to place multiple buttons at
   equal spacing along a line (Shift-drag spacing in some versions).
2. **Buttonhole** tool: place on the overlapping piece; set orientation (vertical for shirt
   plackets, horizontal for jacket fronts).
3. Select a button to set **properties**: shape (from library or imported OBJ), size in mm
   (or ligne equivalent), thickness, colour, metallic/plastic material; buttonhole: length,
   type (straight, keyhole), thread colour.

## Fastening
- **Fasten Button** tool: click a button then its buttonhole; CLO links them so simulation
  pulls the placket closed. Unfasten to open the garment.
- Order: fasten after both sides are arranged and simulated roughly.

## Accuracy
- Use the same button spacing and placket overlap as the tech pack (overlap = button
  diameter in most shirts).
- Attach button OBJs scaled correctly; custom brand buttons can be modelled and imported.

## Gotchas
- Buttonholes on the wrong side (women's left over right vs men's right over left).
- Fastening before arranging both fronts causes pieces to fly across.
- Many high-poly button OBJs slow rendering; use simplified geometry.

## Verify
- [ ] Button size, spacing and placement match the tech pack.
- [ ] Buttons fastened; placket closes without pulling.
- [ ] Correct overlap direction for the garment's gender convention.
