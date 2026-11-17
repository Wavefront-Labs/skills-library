---
id: engineering-technology.aerospace-engineering.orbital-mechanics.porkchop-plot-construction
name: porkchop-plot-construction
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [porkchop, porkchop-plot, launch-window, c3, interplanetary-trajectory, launch-and-rendezvous]
level: practitioner
status: verified
description: "Build a porkchop plot of C3 and arrival speed against launch and arrival dates using Lambert solutions and planetary ephemerides."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "NASA NAIF SPICE (site root: naif.jpl.nasa.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Porkchop plots

**Goal:** visualise the launch and arrival date combinations and their energy cost.

## Method
1. Define grids of departure dates `t_d` and arrival dates `t_a` (time of flight `t_a - t_d`).
2. For each pair get the planet positions from an ephemeris (JPL DE kernels through SPICE).
3. Solve Lambert's problem (see lambert-problem-solver) for the transfer between the positions; take the prograde (short-way) solution.
4. Compute the departure `v_inf_d = |v_transfer,d - v_planet,d|` and arrival `v_inf_a`; launch energy `C3 = v_inf_d^2`.
5. Contour `C3`, `v_inf_a` and time of flight on the date grid; the "porkchop" islands mark the feasible windows.

## Reading the plot
- The minimum-energy region repeats at the synodic period (for Earth-Mars 779.9 days, 25.6 months, computed from sidereal periods).
- A Hohmann-type Earth-Mars transfer has an Earth departure `v_inf` of 2.94 km/s, a `C3` of 8.7 km^2/s^2 (computed with circular coplanar orbits, Mars at 1.5237 AU); real windows have `C3` somewhat above this because of eccentricity and inclination.
- Constrain the plot to launcher capability (`C3` limit), arrival speed (entry or capture delta-v), and time of flight.

## Gotchas
- Multi-revolution Lambert solutions and singularity near 180 degree transfer angle need handling.
- Use consistent time systems (TDB) for ephemerides.
- Pick contour levels around the minimum, not the full range.

## Verify
- [ ] The minimum-energy point agrees with a Hohmann estimate to within the eccentricity effects.
