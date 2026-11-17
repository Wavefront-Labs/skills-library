---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.border-and-basin-irrigation-design
name: border-and-basin-irrigation-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, border-irrigation, basin-irrigation, unit-inflow, border-strip, level-basin, cutoff-ratio, surface-irrigation-design]
level: advanced
status: gated
description: "Design border strips and level basins: unit flow, strip length and width, required time, cutoff and field slope, with checks for ponding and tailwater."
sources:
  - "Walker & Skogerboe, Surface Irrigation: Theory and Practice"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Border and basin irrigation design

**Goal:** a layout and inflow that covers the field quickly and evenly, within the pump or delivery limits.

## Borders
- Long, graded strips between levees. Choose unit flow (flow per metre of strip width) so advance takes about a quarter to a third of the required intake opportunity time at the field end (gated: unconfirmed, source is paywalled or blocked), a rule of thumb; verify with a model (WinSRFR) for your soil.
- Strip width is set by cross-slope (kept level), machinery and available flow; length by soil and slope.
- Cutoff when advance reaches a set fraction of the length (cutoff ratio, often around 0.7 to 0.95 depending on soil and slope (gated: unconfirmed, source is paywalled or blocked)), letting water run out into the remaining length by stored head.

## Level basins
- Zero slope, bounded by levees, filled quickly (high flow); uniform if the fill is fast relative to infiltration. Basin size is limited by the inflow: Q must fill the area to the required depth within a time that gives acceptable uniformity.
- Best on moderate to low intake soils; very high intake soils need very short fill times.

## Practice
- Land grading precision (laser levelling) determines the achieved efficiency; see `land-leveling-and-grade-design`.
- Ponding at the end and tailwater need drainage or re-use; maintain levees.

## Verify
- [ ] Advance and recession measured at the first irrigation and compared to design.
- [ ] Uniformity (low-quarter DU) computed.
- Unconfirmed: the cutoff ratio and flow rules of thumb depend on soil; use local trials.
