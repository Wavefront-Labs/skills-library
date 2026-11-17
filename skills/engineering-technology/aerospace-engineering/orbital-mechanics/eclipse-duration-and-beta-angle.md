---
id: engineering-technology.aerospace-engineering.orbital-mechanics.eclipse-duration-and-beta-angle
name: eclipse-duration-and-beta-angle
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, constellation-design, constellations, coverage, eclipse-geometry, beta-angle, eclipse-duration, sun-geometry]
level: practitioner
status: verified
description: "Compute eclipse fraction and duration for circular orbits from altitude and beta angle, and use it for power, thermal and battery sizing."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Recomputed in Python"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Eclipse duration and beta angle

**Goal:** time in Earth's shadow per orbit.

## Beta angle
`beta` is the angle between the orbit plane and the Sun vector (`sin(beta) = cos(delta_sun) sin(i) sin(Omega - alpha_sun) + sin(delta_sun) cos(i)`). Eclipses vanish when `|beta|` exceeds `beta* = asin(R/(R + h))` (about 70 degrees at 400 km).

## Circular orbit eclipse fraction (cylindrical shadow)
`f_ecl = (1/pi) arccos( sqrt(h^2 + 2 R h) / ((R + h) cos(beta)) )` for `|beta| < beta*`, with `h` altitude, `R` Earth radius. Maximum at `beta = 0`: 0.390 of the orbit at 400 km altitude (36.1 minutes of a 92.56-minute orbit, computed); `beta*` at 400 km is 70.2 degrees.

## Use
1. Compute eclipse and sunlight durations over the mission lifetime (beta varies through the year and with RAAN drift).
2. Battery depth-of-discharge cases use the longest eclipse; solar array sizing uses the shortest sunlight time per orbit.
3. Thermal: hot and cold cases from beta extremes.

## Gotchas
- The cylindrical shadow ignores penumbra (minor for LEO); high-fidelity models include it.
- Sun-synchronous orbits have nearly constant beta for fixed LTAN with seasonal change.

## Verify
- [ ] At `beta = 0`, `h = 400 km` the formula returns about 0.39.
