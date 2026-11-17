---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.traction-limited-launch
name: traction-limited-launch
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [launch-traction, traction-limit, weight-transfer, longitudinal-load-transfer, drive-wheel-friction, awd-launch]
level: practitioner
status: verified
description: "Compute the maximum launch acceleration from tyre friction and longitudinal weight transfer for FWD, RWD and AWD layouts, and compare with powertrain torque."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Traction-limited launch

1. Normal loads on the driven axle at acceleration a: with CG-to-front-axle distance `lf`, CG-to-rear-axle `lr`, wheelbase L, CG height h: `Fz_r = m*(g*lf + a*h)/L`, `Fz_f = m*(g*lr - a*h)/L`.
2. RWD limit: `F_max = mu*Fz_r`, solve `m*a = mu*m*(g*lf + a*h)/L` -> `a = mu*g*lf/(L - mu*h)`.
3. FWD limit: `a = mu*g*lr/(L + mu*h)`.
4. AWD (full lock): `a = mu*g` (ignoring pitch and driveline losses), limited by torque split in practice.
5. Compare with powertrain-limited acceleration `a = (T*i*eta/Re - road load)/(m + m_r)`; the lower governs 0-100 km/h time. Compare both limits; whichever is lower governs.
6. Include tyre peak friction vs surface, launch control strategy (slip target from tyre data), and suspension anti-squat.

**Gotchas:** use measured mu for the actual tyre and surface. Checks: with mu = 1, h/L = 0.2, RWD gives 0.5 g at 40% rear weight and 0.625 g at 50%; FWD with 60% front weight gives 0.5 g (computed).

## Verify
- [ ] Calculated launch acceleration within about 10% of measured in the test.
- [ ] Axle load with transfer matches measured load cell/pitch.
