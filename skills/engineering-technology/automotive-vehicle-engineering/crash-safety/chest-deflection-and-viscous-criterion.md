---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.chest-deflection-and-viscous-criterion
name: chest-deflection-and-viscous-criterion
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [chest-deflection, viscous-criterion, rib-deflection, thoracic-injury, chest-acceleration, v-c]
level: practitioner
status: gated
description: "Evaluate thoracic injury from chest deflection, deflection rate and viscous criterion, with filter classes, dummy-specific limits and design levers."
sources:
  - "FMVSS 208 and UN R94/R95 thoracic criteria; Euro NCAP assessment protocols; confirm current limits"
  - "https://www.law.cornell.edu/cfr/text/49/571.208"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Chest deflection and the viscous criterion

1. Measures: sternum or rib deflection (mm) from the dummy's chest potentiometer or IR-TRACC, filtered CFC 600; chest acceleration (3 ms clip) in some regulations; **viscous criterion** `V*C = V(t)*C(t)` where V is compression velocity and C is normalised compression (deflection/ chest depth), the maximum over time.
2. Limits: FMVSS 208 limits sternum compressive deflection to 63 mm (2.5 in) for the 50th male Hybrid III (S6.4) and 52 mm (2.0 in) for the 5th female (S15.3.4), and chest resultant acceleration to 60 g except for intervals under 3 ms (checked in 49 CFR 571.208). UN R95 side impact uses rib deflection and V*C limits; confirm the values in the current text (gated: unconfirmed, source is paywalled or blocked). Consumer ratings use graded scales.
3. Interpretation: deflection correlates with rib fracture probability by age; the elderly are more vulnerable, so consumer programmes use stricter limits.
4. Design levers: belt load limiter force, belt geometry, airbag stiffness and venting, steering column collapse, side airbag pressure and door padding.
5. Data handling: ensure sensor zero before test, filter correct, remove offset, check polarity.
6. Cross-check against chest acceleration and belt force traces for plausibility.

**Gotchas:** chest deflection can be affected by belt/airbag interaction, not just belt force.

## Verify
- [ ] Reported deflection checked against belt force and acceleration for consistency.
- [ ] Filter class and dummy type recorded.
