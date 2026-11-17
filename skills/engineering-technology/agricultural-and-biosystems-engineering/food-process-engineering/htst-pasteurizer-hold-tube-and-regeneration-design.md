---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.htst-pasteurizer-hold-tube-and-regeneration-design
name: htst-pasteurizer-hold-tube-and-regeneration-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, htst-pasteurization, thermal-processing, canning-process, hold-tube, regenerator, flow-diversion-valve, milk-pasteurization]
level: practitioner
status: gated
description: "Design an HTST pasteuriser: hold-tube length from flow and residence time, regeneration percentage, pressure differential, flow diversion and verification checks."
sources:
  - "https://www.ecfr.gov/current/title-21/part-1240/section-1240.61"
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Singh & Heldman, Introduction to Food Engineering"
  - "US FDA food safety regulations (https://www.fda.gov)"
  - "https://oregon.gov/oda/Documents/Publications/FoodSafety/HTSTStudyGuideENG.pdf"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# HTST pasteuriser hold tube and regeneration design

**Goal:** legal time and temperature for every particle, with safe flow diversion and efficient heat recovery.

## Hold tube
- Required conditions: 21 CFR 1240.61(b) lists 63 C (145 F) 30 min, 72 C (161 F) 15 s, 89 C (191 F) 1 s, 90 C (194 F) 0.5 s, 94 C (201 F) 0.1 s, 96 C (204 F) 0.05 s and 100 C (212 F) 0.01 s; the first two rise by 3 C (5 F) for products with 10 percent or more fat or added sweeteners (fetched, eCFR). Grade A milk follows the PMO and other products and jurisdictions have their own times; check the applicable regulation.
- Length: `L = v_max x t` where v_max is the fastest-particle velocity (not the mean). For turbulent flow v_max is about 1.2 times mean velocity (1/7 power-law profile gives 8x15/98 = 1.224, computed); regulations require measurement by salt conductivity timing for the actual hold tube and pump. Slope the tube upward in the flow direction (the PMO specifies a minimum slope; confirm the value in the current PMO) (gated: unconfirmed, source is paywalled or blocked).
- Pump size and flow limit set by timing tests at the maximum rate, with a timing pump or flow controller to prevent exceeding the rated flow.

## Regeneration
Raw product is warmed by outgoing hot pasteurised product. `Regeneration % = (T_regen out - T_in) / (T_pasteurise - T_in) x 100`. Typical regeneration is high for milk (gated: unconfirmed, source is paywalled or blocked). Higher regeneration saves energy but demands careful pressure control to avoid cross-contamination.

## Safety controls
1. Flow diversion valve diverts product to raw side if temperature falls below set point.
2. Pressure: pasteurised side pressure must exceed the raw side in the regenerator (the PMO sets a minimum differential; confirm the value in the current PMO) (gated: unconfirmed, source is paywalled or blocked), enforced with booster pump and pressure switches.
3. Recording thermometer and indicating thermometer, calibrated and sealed.
4. Verification: alkaline phosphatase test and periodic official testing.

## Gotchas
- Fouling raises pressure drop and changes flow; cleaning cycle times matter.
- Do not alter hold-tube configuration without re-testing.

## Verify
- [ ] Hold-time test result is within the legal minimum at maximum flow.
