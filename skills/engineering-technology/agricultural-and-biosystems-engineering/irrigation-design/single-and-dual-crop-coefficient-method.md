---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.single-and-dual-crop-coefficient-method
name: single-and-dual-crop-coefficient-method
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, dual-crop-coefficient, crop-water-requirements, evapotranspiration, kc, kcb, fao-56, crop-stages, soil-evaporation]
level: practitioner
status: gated
description: "Compute crop ET with FAO-56 single or dual Kc: growth stage lengths, Kc ini mid end, climate adjustment, basal Kcb and soil evaporation Ke, and stress factor Ks."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org)"
  - "FAO Irrigation and Drainage Paper 56, Crop evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Single and dual crop coefficient method

**Goal:** ETc for scheduling or design from ET0 and a defined crop curve.

## Single Kc
`ETc = Kc x ET0`. Build the curve: Kc ini (flat), development (linear), Kc mid (flat), late season (linear to Kc end). Stage lengths come from FAO-56 tables and should be adapted to local planting dates and cultivars; take values from the paper rather than memory.

Adjust tabulated mid and end values for climate:
`Kc mid = Kc mid(Tab) + [0.04 (u2 - 2) - 0.004 (RHmin - 45)] (h / 3)^0.3` where h is crop height (m). The adjustment matters when RHmin differs from 45 percent or u2 from 2 m/s, within the FAO-56 limits 1 <= u2 <= 6 m/s, 20 <= RHmin <= 80 percent and 0.1 m < h < 10 m (FAO-56 chapter 6, Eq. 62). The 0.45 threshold in FAO-56 applies to Kc end (Eq. 65 is used only when tabulated Kc end exceeds 0.45), not to Kc mid.

## Dual Kc
`ETc = (Ks x Kcb + Ke) x ET0`
- **Kcb**: basal coefficient (transpiration plus small evaporation from dry surface).
- **Ke**: evaporation from wet soil surface after rain or irrigation, limited by Kc max and by the exposed, wetted fraction few. Needs a daily soil-surface water balance of the evaporating layer.
- **Ks**: water-stress coefficient; 1.0 if root-zone depletion is below RAW (see TAW and RAW skill).
Use dual Kc where wetting is frequent and canopy is incomplete (drip on young crops, frequent light sprinkler) or when partial wetting is critical; single Kc is adequate for infrequent, heavy irrigation.

## Practice
Spreadsheet or CROPWAT and AquaCrop-type tools implement these; check one season against measured soil moisture.

## Gotchas
- Cover crops and weeds between rows add transpiration that is not in standard Kc.
- Orchards with ground cover: apply density coefficient adjustments (FAO-56 chapter 9).

## Verify
- [ ] Stage dates match local phenology.
- [ ] Seasonal ETc total matches known local crop water use within about 10 percent (gated: unconfirmed, source is paywalled or blocked).
