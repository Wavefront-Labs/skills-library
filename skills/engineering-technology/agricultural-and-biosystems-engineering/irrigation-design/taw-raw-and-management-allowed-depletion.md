---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.taw-raw-and-management-allowed-depletion
name: taw-raw-and-management-allowed-depletion
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, management-allowed-depletion, soil-water, irrigation-scheduling, taw, raw, field-capacity, wilting-point, root-zone]
level: practitioner
status: verified
description: "Compute total and readily available water from soil constants and root depth, set management allowed depletion by crop and ETc, and convert to irrigation interval and depth."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org)"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "FAO Irrigation and Drainage Paper 56, Crop evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TAW, RAW and management allowed depletion

**Goal:** know how much water the root zone holds and how far to let it deplete.

## Formulas
- `TAW = 1000 (theta_FC - theta_WP) Zr` (mm), with theta in m3/m3 and Zr rooting depth in m.
- `RAW = p TAW` (FAO-56 Eq. 82 and 83) where p is the depletion fraction (FAO-56 tabulates p per crop at an ETc of 5 mm/day; adjust `p = p(table) + 0.04 (5 - ETc)`, ETc in mm/day, limited to 0.1-0.8; FAO-56 chapter 8).
- Management allowed depletion (MAD) is the percentage of available water you let go before irrigating; MAD is often set at or below the p value, lower for shallow-rooted, high-value or stress-sensitive crops and for drip.

## Steps
1. Get soil water constants by texture from a soil survey or measure (pressure plate, field capacity by wetted profile after drainage, wilting point at -1500 kPa). Use measured data where soils vary.
2. Use the effective root depth for the crop stage and soil limits (rooting restrictions).
3. Interval for a given rate: `interval = RAW / ETc`; depth per irrigation = depletion refilled to field capacity.
4. Account for layered soils: sum layer by layer.

## Gotchas
- Field capacity and wilting point from tables or different sources can differ substantially; field measurement pays.
- For design, use the shallowest root depth at the peak ETc period.
- Over-irrigating beyond FC loses water to deep percolation and leaches nutrients.

## Verify
- [ ] Soil moisture sensor data show depletion hovering near, not far below, the MAD target.
