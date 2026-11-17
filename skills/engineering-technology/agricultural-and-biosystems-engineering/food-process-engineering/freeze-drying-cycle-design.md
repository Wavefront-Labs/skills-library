---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.freeze-drying-cycle-design
name: freeze-drying-cycle-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, freeze-drying, food-drying, dehydration, lyophilization, primary-drying, sublimation, collapse-temperature, condenser]
level: practitioner
status: draft
description: "Design a freeze-drying cycle: freezing, primary drying below collapse temperature with shelf and pressure control, secondary drying, condenser capacity and end-point detection."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Earle, Unit Operations in Food Processing"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Freeze-drying cycle design

**Goal:** a dry product with preserved structure and minimum cycle time.

## Stages
1. **Freezing**: below the eutectic or glass-transition temperature of the maximally freeze-concentrated solution; freezing rate sets ice crystal size (slow freezing: large crystals, faster primary drying).
2. **Primary drying (sublimation)**: lower chamber pressure (typically about 5-50 Pa (gated: unconfirmed, source is paywalled or blocked); maker and product specific), supply heat of sublimation (approx. 2.83 MJ/kg of ice: vaporisation 2.50 MJ/kg at 0 C, computed with CoolProp, plus fusion about 0.33) through shelves, radiation or microwaves. Keep product temperature at the ice interface below the collapse (or eutectic) temperature.
3. **Secondary drying (desorption)**: raise shelf temperature to remove bound water down to a final moisture of often 1-5 percent (gated: unconfirmed, source is paywalled or blocked).

## Design parameters
- Shelf temperature and chamber pressure interplay: higher pressure improves heat transfer to product but raises product temperature.
- Mass transfer resistance of the dried layer sets sublimation rate; product temperature is estimated by pressure rise tests or thermocouples.
- **Condenser** must trap all vapour: capacity in kg ice, surface temperature around -50 to -80 C (gated: unconfirmed, source is paywalled or blocked); defrost cycles.
- **Vacuum pump** sized for non-condensables and leaks.

## End-point
Monitor Pirani vs capacitance gauge ratio (they converge at the end of sublimation), product thermocouples approaching shelf temperature, or pressure rise test.

## Gotchas
- Operating above collapse temperature ruins structure.
- Load heterogeneity across shelves (edge effect) changes drying times.
- Freeze drying is energy intensive; use for high-value products.

## Verify
- [ ] Residual moisture (Karl Fischer or oven) and water activity within specification.
