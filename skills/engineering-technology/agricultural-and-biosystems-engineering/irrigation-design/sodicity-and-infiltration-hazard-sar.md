---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.sodicity-and-infiltration-hazard-sar
name: sodicity-and-infiltration-hazard-sar
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, sodium-adsorption-ratio, sar, sodicity, infiltration-hazard, irrigation-water-quality, gypsum, fao-29]
level: advanced
status: verified
description: "Assess irrigation water for infiltration problems: SAR and EC together, the FAO 29 guideline, adjusted SAR, gypsum treatment and soil sampling."
sources:
  - "Ayers & Westcot, FAO Irrigation and Drainage Paper 29: Water Quality for Agriculture (https://www.fao.org)"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "FAO Irrigation and Drainage Paper 29 Rev. 1, Water quality for agriculture (https://www.fao.org/4/t0234e/t0234e00.htm)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sodicity and infiltration hazard SAR

**Goal:** decide if the water will cause surface sealing and low intake, and what to do about it.

## Calculation
SAR = Na / sqrt((Ca + Mg)/2), with concentrations in meq/L. Compare with the electrical conductivity of the water (ECw): infiltration falls as SAR rises and also falls when ECw is very low (FAO 29 notes ECw below 0.2 dS/m almost always causes infiltration problems; its Table 1 bands, for example SAR 6-12 with ECw above 1.9 no restriction, 1.9-0.5 slight to moderate, below 0.5 severe). FAO Irrigation and Drainage Paper 29 (Ayers and Westcot, 1985) gives a SAR versus ECw table showing no, slight to moderate, and severe restriction zones; use that table.

## Refinements
Bicarbonate in the water raises the effective sodium hazard through calcium precipitation. The 1976 adjusted SAR with pHc is no longer recommended in FAO 29 Rev. 1 (1985); it prefers the adjusted RNa of Suarez (1981), which uses the Cax value from its Table 11, and still accepts plain SAR for most waters. Soil texture matters: clays are more sensitive than sands.

## Management
- Gypsum or other calcium sources applied to the soil or injected in the water raise the calcium and electrolyte level.
- Sulphur or acidifying amendments can help on calcareous soils (agronomic advice needed).
- Organic matter, residue cover and reducing intensive tillage lessen sealing; sprinkler droplet energy worsens crusting.
- Sample soil exchangeable sodium percentage (ESP) to follow the effect.

## Verify
- [ ] Lab report includes Na, Ca, Mg, HCO3, EC and pH.
- [ ] Infiltration measured before and after treatment (`infiltration-measurement-and-models`).
- Crop-specific thresholds: use the FAO 29 tables.
