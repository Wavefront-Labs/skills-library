---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.land-leveling-and-grade-design
name: land-leveling-and-grade-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, land-leveling, laser-grading, grade-design, plane-method, cut-and-fill, earthwork-balance]
level: practitioner
status: gated
description: "Design land leveling for surface irrigation: topographic survey, plane or profile fit by least squares, cut and fill balance, grade choice and laser control."
sources:
  - "Walker & Skogerboe, Surface Irrigation: Theory and Practice"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Land leveling and grade design

**Goal:** a finished surface with a uniform grade that makes surface irrigation uniform and drains the field, with balanced earthwork.

## Steps
1. Survey the field on a grid (spacing appropriate to the relief; RTK GNSS or laser levels). Record elevations and soil depth information.
2. Choose the design grade along and across the irrigation direction: levels for basins, small continuous slope for borders and furrows. Soils, erosion, cross-slope and drainage dictate the limits.
3. Fit a plane (or planes or a profile) by least-squares to minimise earthwork, then adjust for the chosen grades and field geometry.
4. Compute cuts and fills at each grid point. Balance cut and fill with an allowance for compaction or shrinkage of fill (a factor determined locally, not assumed).
5. Check cut depth against topsoil depth to avoid exposing poor subsoil; limit deep cuts or plan to redistribute topsoil.
6. Execute with laser-controlled scrapers or GNSS machine control; do a final fine pass.

## Practice
- Maintain a cut and fill map for the contractor; check with a post-grading survey.
- Fertility may need correction in deep-cut areas.

## Verify
- [ ] Finished surface within tolerance (set the tolerance with the design; typical laser-grading tolerances are a few centimetres (gated: unconfirmed, source is paywalled or blocked)).
- [ ] Post-grade survey recorded.
- Tolerances and compaction factors vary by soil; take them from local practice or the NRCS handbook (gated: unconfirmed, source is paywalled or blocked).
