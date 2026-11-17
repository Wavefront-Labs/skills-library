---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.quarter-car-ride-model
name: quarter-car-ride-model
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [quarter-car, quarter-car-model, ride-model, ride-frequency, wheel-hop, sprung-mass, unsprung-mass]
level: practitioner
status: gated
description: "Build and solve a quarter-car model for body bounce and wheel-hop frequencies, damping ratio and transmissibility to size springs and dampers."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "Genta, Motor Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Quarter-car ride model

Parameters: sprung mass `ms`, unsprung mass `mu`, suspension rate `ks`, damper `cs`, tyre rate `kt`.

1. Ride rate `kr = ks*kt/(ks + kt)`; body frequency `fb ~ (1/2pi)*sqrt(kr/ms)`. Passenger cars often target roughly 1.0-1.5 Hz (comfort targets differ by segment; check your programme) (gated: unconfirmed, source is paywalled or blocked).
2. Wheel-hop frequency `fw ~ (1/2pi)*sqrt((ks + kt)/mu)`, typically around 10-15 Hz (gated: unconfirmed, source is paywalled or blocked); formula computed (ms 400 kg, mu 40 kg, ks 25 kN/m, kt 200 kN/m gives fb 1.19 Hz, fw 11.9 Hz).
3. Damping ratio of the body `zeta = cs/(2*sqrt(ks*ms))`; 0.2-0.4 is a typical range for ride comfort and body control (gated: unconfirmed, source is paywalled or blocked).
4. State-space: states `zs, zs_dot, zu, zu_dot`, input road `zr`. Use `tf`/`bode` to get body acceleration and tyre deflection transfer functions.
5. Trade-off: body acceleration (comfort), suspension travel (packaging) and tyre dynamic load (grip) cannot all be improved together; plot all three vs damping.

**Gotchas:** forgetting motion ratio: use wheel rates, not spring rates.

## Verify
- [ ] Peaks in the transmissibility plot match the hand-computed fb and fw.
- [ ] Dynamic tyre load stays well below static load (no wheel-lift) on the design bump.
