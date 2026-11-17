---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.top-speed-and-gearing-limits
name: top-speed-and-gearing-limits
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [top-speed-gearing, top-speed, gearing, power-curve, road-load-power, overdrive, gear-selection]
level: practitioner
status: verified
description: "Find top speed from the intersection of engine power at the wheels with road-load power, and choose top-gear ratio for top speed versus economy."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Top speed and gearing limits

1. Wheel power available in gear k: `P_w = P_eng(n)*eta_driveline` with `v = n*2*pi*Re/(60*i_k*i_f)` (n in rpm, Re in m).
2. Road-load power: `P_rl(v) = (A + B*v + C*v^2)*v` (plus grade term for gradeability checks).
3. Top speed is where the available power curve meets `P_rl`. If the intersection is **before** peak power speed (engine speed lower than power peak), the gear is "overdriven": it improves economy but top speed is below the maximum. If beyond peak power the gear is too short: engine speed is past the power peak at top speed, power is falling, and a taller top gear *gains* top speed until the intersection reaches the peak.
4. Best top speed: choose gearing so the intersection falls at the power peak (checked numerically with a cubic power curve and cubic road load: top speed peaks at n/n_peak = 1.005; 20% shorter or 25% taller gearing both lose top speed).
5. Economy-oriented top gear: pick a ratio that puts the cruise speeds of interest near the lowest-BSFC region while keeping reserve acceleration.
6. Check electronic speed limiters, tyre speed rating and driveline limits.

**Gotchas:** driveline efficiency drops at high torque/low speeds; tyre growth at speed raises Re.

## Verify
- [ ] Computed top speed within a few percent of tested top speed on a flat run.
- [ ] Engine speed at top speed below the redline.
