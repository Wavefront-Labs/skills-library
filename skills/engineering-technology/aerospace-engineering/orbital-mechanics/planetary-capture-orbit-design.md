---
id: engineering-technology.aerospace-engineering.orbital-mechanics.planetary-capture-orbit-design
name: planetary-capture-orbit-design
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [capture-orbit, orbit-insertion, hyperbolic-approach, periapsis-burn, aerobraking, interplanetary]
level: practitioner
status: verified
description: "Design a planetary capture orbit insertion burn and choose capture orbit size, with the follow-up trimming and aerobraking options."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Checked algebraically and numerically in Python against the vis-viva relation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Capture orbits

**Goal:** the insertion burn that converts a hyperbolic approach into a bound orbit.

## Insertion burn at periapsis
`dv = sqrt(v_inf^2 + 2 mu/r_p) - sqrt(mu (1 + e)/r_p)` for a target orbit of eccentricity `e` and periapsis radius `r_p`.
- Fixed `r_p` and `v_inf`: higher `e` (larger capture orbit) costs less delta-v (the subtracted term `sqrt(mu (1+e)/r_p)` grows with `e`; limit `e -> 1` is the cheapest, a parabolic capture).
- The minimum for a circular orbit is `sqrt(v_inf^2 + 2mu/r_p) - sqrt(mu/r_p)`.

## Procedure
1. Take `v_inf` from the approach trajectory design.
2. Choose `r_p` (altitude with margin above the atmosphere and for the target science orbit).
3. Choose capture `e` or period from operations constraints (communication, eclipse, time to science).
4. Compute `dv` and propellant mass.
5. Plan the reduction to the science orbit: periapsis burns lower the apoapsis, apoapsis burns change the periapsis and plane (cheap at low speed), or use aerobraking, which trades propellant for months of atmospheric passes at a controlled drag limit.
6. Add a margin for navigation errors and a contingency orbit-insertion strategy.

## Gotchas
- The insertion burn is time-critical, and often happens behind the planet out of contact.
- Targeting periapsis requires an approach navigation plan; errors cost either impact risk or a miss.
- Aerobraking needs a thermal and structural limit on the spacecraft and an atmosphere density model with real-time update.

## Verify
- [ ] Post-burn orbit from vis-viva has the intended period and periapsis.
