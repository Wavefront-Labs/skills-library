---
id: creative-arts.photography-fine-art.art-photography.hyperfocal-distance-focusing
name: hyperfocal-distance-focusing
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, depth-of-field, hyperfocal-distance, circle-of-confusion, zone-focusing, dof-calculator, landscape-focus]
level: practitioner
status: draft
description: "Compute and use hyperfocal distance (with a realistic circle of confusion) to keep foreground to infinity acceptably sharp in landscapes."
sources: ["https://www.dofmaster.com/hyperfocal.html", "https://en.wikipedia.org/wiki/Hyperfocal_distance", "Ansel Adams, The Camera (depth of field)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hyperfocal distance focusing

**Hyperfocal distance H** = focus distance at which depth of field extends from H/2 to
infinity.

    H = f^2 / (N x c) + f        (f focal length, N f-number, c circle of confusion, same units)

## Circle of confusion
- Default calculators use c = 0.030 mm on full frame (from an 8x10 inch print at
  25 cm viewing). For **large fine-art prints**, halve it (0.015 mm) or more, otherwise
  "infinity" looks soft.
- APS-C ~0.020 mm default; 4x5 ~0.1 mm.

## Example
24 mm, f/11, c = 0.030: H = 576 / 0.33 = 1745 mm, about 1.75 m; sharp from 0.87 m to infinity.
With c = 0.015 for big prints: H about 3.5 m; sharp from 1.75 m.

## Procedure
1. Pick c for your intended print size.
2. Calculate H (app such as PhotoPills or a printed table).
3. Focus at H using the distance scale, live view magnification on an object at that
   distance, or by laser rangefinder.
4. Check the far distance at 100% in live view; slight rear softness means focus a bit further.

## Gotchas
- Many lens distance scales are inaccurate or absent (focus-by-wire). Use a measured object.
- Hyperfocal gives *acceptable* sharpness everywhere, *maximum* nowhere. When the far
  horizon must be critically sharp, focus slightly beyond H or focus-stack instead.
- Stopping down past about f/11-f/16 on full frame trades DoF for diffraction softness.

## Verify
- [ ] Nearest important foreground and distant horizon both sharp at intended print size.
