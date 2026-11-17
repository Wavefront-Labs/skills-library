---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.sprinkler-spacing-and-layout-design
name: sprinkler-spacing-and-layout-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, sprinkler-spacing, sprinkler-design, sprinkler-irrigation-design, set-spacing, wetted-diameter, solid-set, hand-move, nozzle-selection]
level: practitioner
status: gated
description: "Choose sprinkler spacing and pattern from wetted diameter and wind, select nozzle and pressure from the manufacturer's chart, and check application rate and uniformity."
sources:
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "NRCS Conservation Practice Standard 442, Sprinkler System, Vermont 2017 (https://efotg.sc.egov.usda.gov/api/CPSFile/21967/442_VT_CPS_Sprinkler_System_2017)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sprinkler spacing and layout design

**Goal:** uniform coverage at an application rate the soil accepts.

## Steps
1. **Wetted diameter** from the manufacturer's performance data for nozzle size and pressure.
2. **Spacing** as a percentage of wetted diameter, tightening as wind rises. Use the table in the governing standard: NRCS Standard 442 (Vermont 2017) lists lateral spacing for periodic-move big guns and towpaths of 65 percent at 0-1 mph down to 45 percent above 10 mph (sprinkler spacing 50 percent), and different values for fixed solid-set rectangular and triangular patterns. Triangular gives better uniformity at the same spacing (gated: unconfirmed, source is paywalled or blocked).
3. **Application rate**: `Ia (mm/h) = 1000 q (m3/h) / (S_l x S_m)` with S_l along-lateral and S_m between-lateral spacing in m; or in US units, `Ia (in/h) = 96.3 q (gpm) / (S_l x S_m (ft^2))`.
4. **Check against soil intake** (see the application rate skill).
5. **Nozzle and pressure**: choose from the maker's chart; typical operating pressures for impact sprinklers are about 200-400 kPa (gated: unconfirmed, source is paywalled or blocked). Maintain spacing and pressure so the distribution profile overlaps well.
6. **Lateral and mainline layout**: orient laterals across the prevailing wind direction, and run the lateral along the contour or with slight downslope.
7. Calculate the number of sprinklers per set from the system flow.

## Gotchas
- Wind distorts patterns; reduce spacing and use a lower trajectory angle or smaller droplets only with tests.
- High pressure creates fine droplets (drift and evaporation losses).
- Sprinkler riser height and plant canopy interference alter patterns.

## Verify
- [ ] Catch-can test meets the CU required by the governing standard: NRCS 442 (Vermont 2017) requires CU not less than 75 percent for deep-rooted field and forage crops without chemigation, and 85 percent for high-value or shallow-rooted crops or any crop with fertigation or chemigation.
