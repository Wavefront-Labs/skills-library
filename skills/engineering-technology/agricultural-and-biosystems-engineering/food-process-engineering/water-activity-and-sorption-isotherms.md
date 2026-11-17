---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.water-activity-and-sorption-isotherms
name: water-activity-and-sorption-isotherms
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, water-activity, food-drying, dehydration, sorption-isotherm, gab-model, equilibrium-relative-humidity, shelf-stability]
level: practitioner
status: draft
description: "Measure water activity and fit sorption isotherms with the GAB model, relate aw to microbial growth limits and shelf stability, and use isotherms for drying targets."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Fellows, Food Processing Technology: Principles and Practice"
  - "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-technical-guides/water-activity-aw-foods"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Water activity and sorption isotherms

**Goal:** know the moisture content at which a food is stable and how to dry or package to hold it.

## Water activity
`a_w = p / p_0` (vapour pressure of the food over that of pure water at the same temperature) equals equilibrium relative humidity divided by 100. Measure with a chilled-mirror dew point meter or capacitance sensor at controlled temperature; calibrate with saturated salt standards.

## Microbial guidance
Growth limits (approximate, organism and conditions dependent): most bacteria about 0.91, many yeasts about 0.88, many moulds about 0.80 (xerophilic moulds are reported down to about 0.61-0.65), extreme xerophiles about 0.60-0.70; Staphylococcus aureus can grow aerobically down to about 0.86. Foods below about 0.6 do not support microbial growth. In the US, finished foods held at aw 0.85 or less are outside 21 CFR 108, 113 and 114 (FDA aw inspection guide). Regulatory and product safety assessments must also consider pH and processing.

## Isotherms
1. Equilibrate samples over saturated salt solutions (or use a dynamic vapour sorption instrument) at constant temperature; weigh for equilibrium moisture.
2. Fit models: **GAB** `X = X_m C K a_w / [(1 - K a_w)(1 - K a_w + C K a_w)]` valid to about 0.9; BET up to about 0.4-0.5 (gated: unconfirmed, source is paywalled or blocked).
3. Adsorption and desorption curves differ (hysteresis); dryers follow desorption.
4. Temperature shifts isotherms (moisture at a given aw falls as temperature rises).

## Use
- Set the drying target moisture from the isotherm and the target a_w.
- Predict moisture gain in packages given permeability and storage RH.
- Mixed products: moisture migrates between components with different a_w.

## Verify
- [ ] Measured a_w of the finished product at the dried moisture is below the target with margin.
