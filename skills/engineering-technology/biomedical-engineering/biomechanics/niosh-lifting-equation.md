---
id: engineering-technology.biomedical-engineering.biomechanics.niosh-lifting-equation
name: niosh-lifting-equation
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [niosh-lifting, injury-biomechanics, occupational-biomechanics, recommended-weight-limit, lifting-index, manual-handling, ergonomics]
level: practitioner
status: verified
description: "Compute the revised NIOSH recommended weight limit and lifting index step by step, with multipliers, limits of application and a worked example."
sources: ["Waters, Putz-Anderson, Garg, Fine, Revised NIOSH equation for the design and evaluation of manual lifting tasks (Ergonomics 1993); formulas as reproduced in Waters, Revised NIOSH Lifting Equation, CDC Stacks https://stacks.cdc.gov/view/cdc/193671", "NIOSH, Applications Manual for the Revised NIOSH Lifting Equation (Technical Report 94-110) at https://www.cdc.gov/niosh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NIOSH lifting equation

**Goal:** estimate a recommended weight limit (RWL) for a two-handed manual lift and flag tasks with a lifting index above 1.

Applies to two-handed lifts in a controlled setting; check the limits of application in the NIOSH applications manual (no one-handed, seated, kneeling, unstable loads, high-speed lifting, hot or cold extremes).

## Formula (metric)
RWL (kg) = 23 x HM x VM x DM x AM x FM x CM

- **HM** = 25 / H (H = horizontal distance of hands from the midpoint between the ankles, cm; H below 25 cm is set to 25 cm, so HM = 1; HM = 0.4 at H = 63 cm and the multiplier is 0 beyond)
- **VM** = 1 - 0.003 x |V - 75| (V = vertical hand height at origin, cm; VM = 0 above 175 cm)
- **DM** = 0.82 + 4.5 / D (D = vertical travel distance, cm; D below 25 cm is set to 25 cm; DM = 0.85 at 175 cm)
- **AM** = 1 - 0.0032 x A (A = asymmetry angle in degrees, limited to 0-135; AM = 0 beyond)
- **FM** = frequency multiplier from the NIOSH table (lifts per minute, duration, V)
- **CM** = coupling multiplier from the table (good, fair, poor)
- LI = load weight / RWL. LI above 1 indicates an elevated risk for some workers; higher is worse.

## Worked example
Load 15 kg, H = 40 cm, V = 50 cm, D = 60 cm, A = 0, good coupling, FM 1.0.
HM = 0.625, VM = 0.925, DM = 0.895, AM = 1.
RWL = 23 x 0.625 x 0.925 x 0.895 = 11.90 kg (computed). LI = 15 / 11.90 = 1.26, so redesign (bring the load closer or raise the pallet).

## Procedure
1. Measure at origin and destination of the lift; compute each, and use the worse for single-task analysis.
2. For multi-task jobs use the composite lifting index method from the manual.
3. Redesign priorities: reduce H first (it has the largest effect), then V and D.

## Gotchas
- Using the equation outside H, V, D bounds; a multiplier of 0 means no limit applies.
- Do not use as a pass/fail law: it is a screening and design tool.

## Verify
- [ ] All multipliers in valid ranges.
- [ ] Recalculate after the fix to confirm LI at or below 1.
