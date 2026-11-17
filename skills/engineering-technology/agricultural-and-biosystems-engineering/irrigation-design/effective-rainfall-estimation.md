---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.effective-rainfall-estimation
name: effective-rainfall-estimation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, effective-rainfall, crop-water-requirements, rainfall-analysis, usda-scs-method, dependable-rain, cropwat]
level: practitioner
status: gated
description: "Estimate effective rainfall for irrigation requirement: USDA-SCS monthly formula, fixed-percentage and dependable-rain methods, runoff and deep percolation caveats."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Effective rainfall estimation

**Goal:** the part of rain that actually reduces irrigation demand.

## Methods
1. **Fixed percentage** (e.g. 80 percent of rain): simple; acceptable only for light-rainfall, flat conditions.
2. **Dependable rain**: use rain at a chosen probability of exceedance (often 75-80 percent (gated: unconfirmed, source is paywalled or blocked)) from at least 20-30 years of records, then apply an effectiveness factor.
3. **USDA Soil Conservation Service formula** (monthly, as used by FAO CROPWAT): for monthly rainfall P in mm,
   `Pe = P (125 - 0.2 P) / 125` for `P <= 250 mm`, and `Pe = 125 + 0.1 P` for `P > 250 mm` (gated: unconfirmed, source is paywalled or blocked); FAO's effective-rainfall chapter (fao.org/4/x5560e/x5560e03.htm) documents the USDA-SCS method as a table of monthly rainfall against consumptive use. Also a soil-storage-limited form for daily use with the available soil water.
4. **Daily water balance**: compute runoff (SCS Curve Number) and deep percolation beyond field capacity for each event; effective rain is what raises storage in the root zone and does not run off or percolate (the most defensible method).

## Notes
- Light rainfall events below about 5 mm (gated: unconfirmed, source is paywalled or blocked) are mostly intercepted and evaporated; some methods set them to zero.
- Drip systems wet part of the surface, so rainfall is effective only in the wetted fraction; account for it in dual Kc.
- Intense storms on sloped, crusted soils generate runoff regardless of monthly total.

## Gotchas
- Never use effective rain for peak design flows; design assumes dry spells.
- Monthly formulas hide the effect of storm size.

## Verify
- [ ] Method named in the design report with the rainfall dataset and probability level.
