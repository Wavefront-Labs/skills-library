---
id: engineering-technology.aerospace-engineering.orbital-mechanics.hohmann-transfer
name: hohmann-transfer
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, transfers, orbit-transfers, hohmann, delta-v, transfer-orbit, two-impulse, geo-transfer]
level: practitioner
status: verified
description: "Compute Hohmann transfer burns, time of flight and propellant for coplanar circular orbits, with a LEO to GEO worked example and the limits of the two-impulse model."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "NASA Earth Fact Sheet, https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Hohmann transfer

**Goal:** the minimum-delta-v two-impulse transfer between coplanar circular orbits.

## Formulas (radii `r1 < r2` from the central body's centre)
- `Delta v1 = sqrt(mu/r1) (sqrt(2 r2/(r1 + r2)) - 1)`
- `Delta v2 = sqrt(mu/r2) (1 - sqrt(2 r1/(r1 + r2)))`
- Transfer semi-major axis `a_t = (r1 + r2)/2`; time of flight `TOF = pi sqrt(a_t^3/mu)`.

## Example: 300 km LEO to GEO (`r2 = 42,164 km`)
`Delta v1` about 2.43 km/s, `Delta v2` about 1.47 km/s (circularisation), total about 3.9 km/s; `TOF` about 5.3 hours.

## Practice
1. Add plane change at the apogee burn when inclination must change (combine the plane change with the apogee burn to save delta-v).
2. Convert to propellant mass with the rocket equation.
3. Real transfers use finite burns (gravity losses) and perturbations; use a trajectory tool for the final design.
4. For electric propulsion use a low-thrust spiral model instead.

## Gotchas
- Radii include the central body radius, not just altitude.
- Hohmann is optimal among two-impulse coplanar transfers only; bi-elliptic can beat it at large radius ratios (above 11.94 with a very large intermediate apoapsis, and for any intermediate apoapsis above 15.58; see bi-elliptic-transfer).

## Verify
- [ ] Total `Delta v` equals the difference of circular speed terms computed independently.
