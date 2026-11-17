---
id: creative-arts.fashion-design.draping.digitising-a-trued-drape-into-cad
name: digitising-a-trued-drape-into-cad
category: creative-arts
field: fashion-design
product: draping
tags: [fashion-design, draping, pattern-digitising, digitizer, pattern-cad, dxf-aama, drape-to-flat]
level: practitioner
status: draft
description: "Digitise a trued drape into pattern CAD: preparing paper, digitiser table or photo-digitising, point types, grain and notches, checking scale and exporting DXF-AAMA."
sources:
  - https://en.wikipedia.org/wiki/Digitizer
  - https://en.wikipedia.org/wiki/AutoCAD_DXF
  - https://www.gerbertechnology.com
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Digitising a trued drape into CAD

**Goal:** turn the trued muslin into an accurate CAD pattern that the pattern room and
3D software can use.

## Prepare
1. Transfer the trued drape to pattern card or paper (muslin stretches on a digitiser).
2. Mark on every piece: piece name, size, grainline arrow, notches, drill holes, fold lines,
   and seam lines or cut lines (decide which you digitise; most systems digitise the net
   seam line and add seam allowance in CAD).
3. Flatten creases; tape to the table.

## Digitiser table (Gerber, Lectra, Optitex, Tukatech)
- Cursor buttons set point type: **end/corner** points vs **curve** points, notches, drill
  holes, grainline start/end, internal lines.
- Digitise clockwise; put curve points every 2-3 cm on tight curves, less on gentle ones.
- Close the piece at the start point.

## Photo/scan digitising
- Systems such as photo-digitisers (camera plus calibration board) or flatbed scanning:
  include the calibration marks or a known reference square, shoot square-on, then trace in CAD.
- Check scale: measure a known 10 cm reference line after import.

## After digitising
- Smooth curves, check walking seams and notch alignment in CAD.
- Add seam allowances per seam, name pieces consistently.
- Export **DXF-AAMA/ASTM** for exchange with other CAD systems or CLO 3D.

## Gotchas
- Too few curve points flatten armholes and necklines.
- Muslin digitised directly shrinks or stretches the pattern.
- DXF from different vendors may lose notch types; spot-check after import.

## Verify
- [ ] Every piece measured against the paper at two points.
- [ ] Grain, notches and drill holes present.
- [ ] Exported file opens correctly in the receiving system.
