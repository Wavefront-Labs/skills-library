---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.gear-ratio-spread-and-steps
name: gear-ratio-spread-and-steps
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [ratio-spread, gear-ratio, step-ratio, geometric-progression, first-gear, gear-spacing, transmission-ratios]
level: practitioner
status: gated
description: "Choose first and last gear ratios and the intermediate steps: total spread, geometric and progressive spacing, and the effect on shift quality."
sources:
  - "Naunheimer et al., Automotive Transmissions"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ratio spread and step selection

1. **First gear** from launch/gradeability: required wheel force at max grade or max starting torque, and clutch/converter capability: `i1 >= F_req*Re/(T_max*eta*i_f)`.
2. **Top gear** from top speed / cruise economy (see top-speed-and-gearing-limits).
3. **Spread** `S = i1/in`. More gears allow the same spread with smaller steps and better engine operating points: modern 8-10 speed automatics have spreads of about 7-10 or more (gated: unconfirmed, source is paywalled or blocked) (check data of reference transmissions).
4. **Step** `phi_k = i_k/i_(k+1)`. Geometric spacing uses `phi = S^(1/(n-1))` (constant step; computed: S = 8, n = 8 gives 1.346). Progressive spacing makes steps decrease toward the top gears so the top gears sit close together for cruise.
5. Choose by shift quality: steps of about 1.2-1.6 are typical (gated: unconfirmed, source is paywalled or blocked); large steps give a large rpm drop on shift (noticeable) and lower power-matching.
6. Tractive force diagram: plot F vs v for each gear to check overlap and no power gaps.

**Gotchas:** lower first gear causes high torque at the driveline and clutch heat; check gear durability.

## Verify
- [ ] Tractive-force plot shows overlap between consecutive gears.
- [ ] Engine speed drop after shift is acceptable (for example within a few hundred to a thousand rpm) per spec.
