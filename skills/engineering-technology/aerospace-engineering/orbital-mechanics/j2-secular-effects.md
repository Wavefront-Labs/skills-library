---
id: engineering-technology.aerospace-engineering.orbital-mechanics.j2-secular-effects
name: j2-secular-effects
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, perturbations, orbit-perturbations, j2, nodal-regression, apsidal-rotation, critical-inclination, oblateness]
level: practitioner
status: verified
description: "Compute J2 nodal regression and apsidal rotation, the critical inclination, and use them to choose orbits and plan station-keeping."
sources:
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Montenbruck and Gill, Satellite Orbits"
  - "NASA Earth Fact Sheet, https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html (J2 = 1082.63e-6, R = 6378.137 km)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# J2 secular effects

**Goal:** the dominant long-term perturbation of Earth satellites.

## Rates (mean elements, `p = a (1 - e^2)`, `n = sqrt(mu/a^3)`, `J2 = 1.08263e-3`, `R = 6378.137 km`)
- Node: `Omega_dot = -(3/2) J2 (R/p)^2 n cos(i)` (westward for prograde orbits).
- Perigee: `omega_dot = (3/4) J2 (R/p)^2 n (5 cos^2(i) - 1)`; zero at the critical inclination of 63.4 degrees (and 116.6 degrees), used by Molniya-type orbits.
- Mean motion correction is small but matters for ground-track repetition.

## Use
1. Pick inclination for a desired node drift (sun-synchronous, see that skill).
2. For Molniya, choose `i = 63.4` degrees so apogee stays over the target region.
3. Predict RAAN of a constellation plane drift to design phasing or maintenance.

## Example
At 700 km altitude and 98.2 degrees, `Omega_dot` is about +0.987 degrees/day; exactly 0.9856 degrees/day needs 98.19 degrees (sun-synchronous). Critical inclination: `acos(1/sqrt(5))` = 63.435 degrees (computed).

## Gotchas
- Mean vs osculating elements: formulas use mean elements.
- Higher zonal harmonics, drag and lunisolar terms add to the secular drift at higher accuracy.

## Verify
- [ ] A numerical propagator with J2 only reproduces the node rate within a few percent.
