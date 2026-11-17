---
id: engineering-technology.aerospace-engineering.orbital-mechanics.repeat-ground-track-design
name: repeat-ground-track-design
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [repeat-ground-track, repeat-cycle, revisit, nodal-period, j2, constellation-design]
level: practitioner
status: verified
description: "Choose semi-major axis so the ground track repeats after k revolutions in D days, including J2 effects, and verify with propagation."
sources:
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "USGS Landsat 8, https://www.usgs.gov/landsat-missions/landsat-8"
  - "Recomputed in Python"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Repeat ground tracks

**Goal:** altitude such that the sub-satellite track repeats after `k` orbits in `D` nodal days.

## Condition
The track repeats when `k/D = (omega_E - Omega_dot) / (n_bar + omega_dot)`, where `omega_E` is Earth's rotation rate, `Omega_dot` the nodal regression rate and `omega_dot` the perigee drift from J2; `n_bar` is the mean motion corrected for J2.
- Without J2: `k * T = D * (2 pi/omega_E)`.

## Procedure
1. Choose `k` and `D` (coprime) from the revisit and swath needs.
2. Initial guess `a` from the J2-free relation.
3. Iterate on `a` (solve with a root finder) using the J2 secular rates (see j2-secular-effects) for the inclination and eccentricity.
4. Choose a sun-synchronous inclination if needed, which couples `i` and `a` (see sun-synchronous-orbit-design).
5. Check that altitude lies in a usable range and that drag and stationkeeping can hold the track within the cross-track deadband.
6. Verify with a propagation over several cycles.

## Example
A well-known case: Landsat-class orbits at about 705 km altitude repeat every 16 days (USGS: 705 km, 16-day repeat, sun-synchronous at 98.2 degrees), which is 233 orbits per cycle (14.5625 per day; the Keplerian period at 705 km gives 14.563 per day, computed).

## Gotchas
- Drag lowers altitude, shifting the track; plan altitude-maintenance burns to hold the repeat track within the deadband.
- Eccentric orbits have a changing repeat condition; the frozen-orbit choice fixes `omega`.

## Verify
- [ ] After `D` days the sub-satellite longitude returns to the initial value within the design tolerance.
