---
id: engineering-technology.aerospace-engineering.orbital-mechanics.sun-synchronous-orbit-design
name: sun-synchronous-orbit-design
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, perturbations, orbit-perturbations, sun-synchronous, ltan, local-time, earth-observation, repeat-orbit]
level: practitioner
status: gated
description: "Design a sun-synchronous orbit: required inclination from altitude and eccentricity, local time of the ascending node, and drift of local time over life."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "USGS Landsat 8, https://www.usgs.gov/landsat-missions/landsat-8"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Sun-synchronous orbit design

**Goal:** an orbit whose plane precesses with the Sun, giving constant local solar time.

## Condition
Node rate `Omega_dot = 360 degrees / 365.2422 days = 0.9856 degrees/day`. Using the J2 rate:
`cos(i) = - 2 Omega_dot a^(7/2) (1 - e^2)^2 / (3 J2 R^2 sqrt(mu))`.
Computed results: 98.19 degrees at 700 km and 98.60 degrees at 800 km (circular, J2 only). USGS gives Landsat 8 as sun-synchronous at 705 km, 98.2 degrees. Inclination is retrograde.

## Choose the local time
- Local time of the ascending node (LTAN) is a mission choice: late-morning (about 10:30, low cloud and good lighting), early-afternoon (about 13:30), or dawn-dusk (06:00 or 18:00, nearly constant illumination of the solar arrays) (gated: unconfirmed, source is paywalled or blocked). Landsat 8 crosses the equator at about 10:12 +/- 5 min per USGS.
- Eclipse duration and beta angle depend on LTAN.

## Maintenance
Inclination drifts from lunisolar perturbation and drag; local time drift is corrected by inclination manoeuvres if the mission needs tight local time. Frozen-orbit eccentricity is often combined (eccentricity and perigee argument chosen to hold constant altitude over latitude).

## Procedure
1. Choose altitude (repeat ground track, swath, drag).
2. Solve for inclination.
3. Select LTAN and launch time.
4. Plan drag-makeup and inclination manoeuvres.

## Verify
- [ ] Node rate in a J2 propagation equals 0.9856 degrees/day within 1%.
