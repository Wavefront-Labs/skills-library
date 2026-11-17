---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.air-suspension-design
name: air-suspension-design
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [air-suspension, air-spring, ride-height-control, auxiliary-volume, adaptive-damping, compressor, suspension-types]
level: practitioner
status: verified
description: "Design an air-spring suspension: effective area, rate and frequency, ride height levelling, auxiliary volumes, compressor sizing and failure modes."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis"
  - "air-spring supplier technical documentation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Air suspension

1. Spring rate: `k = n*p*A_eff^2/V + p_g*dA_eff/dz` (derived from F = p_g*A_eff and p*V^n = const) where n is the polytropic exponent (about 1.0 for slow isothermal change to about 1.4 for fast adiabatic), p absolute pressure in the first term, p_g gauge pressure in the second, `A_eff` effective area and V volume. The second term accounts for the shape of the bellow or piston.
2. Load levelling: pressure rises with load to keep ride height; the ride frequency stays nearly constant with load because both rate and load scale roughly with pressure; check by calculation across the load range.
3. Auxiliary volume: a connected reservoir reduces rate (lower frequency) and may use a switchable volume for comfort/sport modes with throttling for damping.
4. Height control: sensors and valve block; fill/dump strategies; time to raise; limits when the engine is off (reservoir or compressor limits); sag when parked and leakage.
5. Compressor: duty cycle and thermal limits, noise isolation, dryer for moisture.
6. Safety: fail-safe ride height, leak detection, travel limit at low pressure (bump stop), regulation about height changes while driving.
7. Combine with adaptive dampers for overall control.

**Gotchas:** temperature affects pressure and height; moisture freezing in valves.

## Verify
- [ ] Rate vs height measured on a spring test rig vs calculation.
- [ ] Levelling time and standing-leak limits tested.
