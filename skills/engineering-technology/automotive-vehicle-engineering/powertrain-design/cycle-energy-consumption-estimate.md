---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.cycle-energy-consumption-estimate
name: cycle-energy-consumption-estimate
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [energy-consumption-estimate, energy-consumption, wh-per-km, wheel-energy, regen-efficiency, cycle-estimate]
level: practitioner
status: gated
description: "Estimate cycle energy consumption by hand: wheel energy from road load and inertia, losses through the drivetrain, regen recovery and auxiliary energy."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Cycle energy consumption estimate

1. Wheel power each second: `P_w = (F_rl(v) + (m + m_r)*a)*v`.
2. Traction energy: sum of positive `P_w` divided by drivetrain efficiency (battery to wheel, typically 0.80-0.90 for EVs (gated: unconfirmed, source is paywalled or blocked); use the map); regen: sum of negative `P_w` times regen efficiency (wheel to battery, including blending limits; often well below the motoring efficiency).
3. Add auxiliary energy: average aux power (a few hundred W of 12 V loads plus HVAC) times cycle time.
4. Net battery energy = traction/eta - regen*eta_r + aux; divide by distance for Wh/km.
5. Sanity check: city cycles show lower consumption from regen but higher from stop-start; motorway speeds are dominated by aero, with aero energy per km rising roughly with v^2 (aero power with v^3).
6. Report on a stated basis (battery DC, or at the wall including charger efficiency).
7. Compare with the simulation to catch modelling errors.

**Gotchas:** negative-power samples not all recoverable (blending, speed threshold, battery limits).

## Verify
- [ ] Hand estimate within about 10% of the full simulation.
- [ ] Basis (DC or AC) stated in the report.
