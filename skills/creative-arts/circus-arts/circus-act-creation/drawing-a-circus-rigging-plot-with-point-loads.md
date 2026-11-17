---
id: creative-arts.circus-arts.circus-act-creation.drawing-a-circus-rigging-plot-with-point-loads
name: drawing-a-circus-rigging-plot-with-point-loads
category: creative-arts
field: circus-arts
product: circus-act-creation
tags: [circus-act-creation, circus-arts, rigging-load-calculation, rigging-plot, point-load, rigging-plan, tech-rider, venue-rigging, cad]
level: practitioner
status: draft
description: "Draw a rigging plot for a circus act: dimensioned point positions, static and dynamic point loads, swing and spin clearances, what venues expect."
sources: ["Harry Donovan, Entertainment Rigging (2002)", "ETCP rigging practice - https://etcp.esta.org", "Venue technical specifications and house rigging policies (typical UK/US touring practice)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drawing a circus rigging plot with point loads

**Goal:** a drawing that lets a venue's rigger decide, before you arrive, whether and how
they can hang your act.

## What the plot must show
1. **Plan view** of the stage with a datum (centre line and setting line / stage edge).
2. **Each point**: ID (P1, P2...), position dimensioned from the datum (x, y), required
   height of the apparatus attachment above the stage.
3. **Loads per point**: static load, design peak (dynamic) load, and direction if not
   vertical (swinging trapeze, bridles, guy lines).
4. **Apparatus type** and what hangs from each point (swivel, rope, hoop).
5. **Clearances**: swing arc, spin radius, flying paths, so the venue keeps lights and
   scenery clear.
6. **Ground anchors**: floor points for guy lines or spanish web, with loads.
7. **Contact** for the act's rigger and revision date.

## Load table example
| Point | Apparatus | Static | Peak | Direction | Height |
|---|---|---|---|---|---|
| P1 | Duo lyra (swivel) | 1.4 kN | 8.5 kN | vertical | 6.0 m |
| P2 | Spanish web | 0.8 kN | 4.0 kN | vertical | 7.5 m |
| G1 | Pole guy | - | 3.0 kN | 45 deg | floor |

## Tools
Vectorworks Spotlight or AutoCAD are standard; a clear hand drawing with dimensions is
better than a confusing CAD file. Export to PDF with a scale bar.

## Gotchas
- Venue beam positions rarely match your ideal points: give a tolerance ("P1 +/- 0.5 m")
  and say what bridle is acceptable.
- Units: state kN and metres explicitly; many venues work in pounds and feet.
- Update the plot for every act change; outdated plots are worse than none.

## Verify
- [ ] Every point has position, height, static and peak loads.
- [ ] Clearances drawn.
- [ ] Revision date and contact on the sheet.
