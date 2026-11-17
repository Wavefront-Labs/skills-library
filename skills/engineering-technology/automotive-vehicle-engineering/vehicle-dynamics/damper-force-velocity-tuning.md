---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.damper-force-velocity-tuning
name: damper-force-velocity-tuning
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [damper-tuning, damper, force-velocity, rebound, compression, damping-ratio, ride-tuning, ride-comfort]
level: practitioner
status: gated
description: "Specify damper force-velocity curves from damping ratio targets, split rebound and compression, and verify on a damper dyno and in the car."
sources:
  - "Dixon, The Shock Absorber Handbook"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Damper force-velocity tuning

1. Start from damping ratio targets: `c_crit = 2*sqrt(k_wheel*m_corner)`; choose zeta body 0.2-0.4 (comfort-oriented lower, handling-oriented higher) as a starting range (gated: unconfirmed, source is paywalled or blocked).
2. Convert to damper force at damper velocity using motion ratio: `c_damper = c_wheel/MR^2` (MR = damper travel / wheel travel).
3. Piecewise curve: low-speed region (body control, up to ~0.1-0.3 m/s) more damping; high-speed region (potholes, wheel control) less, via blow-off valves or progressive digressive curves.
4. Rebound typically greater than compression (a common range is rebound 1.5-3 times compression force (gated: unconfirmed, source is paywalled or blocked); confirm on benchmark cars) because compression force adds directly to input shock.
5. Verify on a damper dyno (sine at set strokes) and look for friction, hysteresis, gas force and temperature dependence.
6. Tune in the car: subjective on varied roads plus objective acceleration/travel data; fix one end at a time.

**Gotchas:** damper friction and bushings dominate small-amplitude ride; measure them.

## Verify
- [ ] Dyno curve falls within the tolerance band of the specification.
- [ ] Ride metrics improve or hold between iterations.
