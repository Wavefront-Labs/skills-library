---
id: engineering-technology.chemical-engineering.reactor-design.trickle-bed-reactor-design
name: trickle-bed-reactor-design
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-multiphase-reactors, trickle-bed-reactor-design, trickle-bed, packed-bed-gas-liquid, catalyst-wetting]
level: practitioner
status: draft
description: "Design a trickle bed reactor: flow regime, liquid holdup, pressure drop, catalyst wetting and heat management."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trickle bed reactor design

**Goal:** Design a trickle bed reactor: flow regime, liquid holdup, pressure drop, catalyst wetting and heat management.

## Steps
1. Confirm trickle flow regime on a flow map (low to moderate gas and liquid rates), not pulsing or bubble flow.
2. Estimate pressure drop and liquid holdup from established correlations (for example Larachi or Sato type) and confirm with the reference.
3. Check catalyst wetting efficiency; poor liquid distribution lowers conversion and creates hot spots.
4. Provide liquid distributors, redistribution between beds, and quench between beds for exothermic reactions.
5. Scale up by keeping liquid hourly space velocity and the superficial liquid velocity ratio in line with the pilot.

## Gotchas
- Maldistribution can give runaway hot spots in hydrotreating type duty.
- Pilot scale data with the real catalyst is needed.

## Verify
- [ ] Regime and wetting checks pass.
- [ ] Bed temperature rise per bed is within limits.
