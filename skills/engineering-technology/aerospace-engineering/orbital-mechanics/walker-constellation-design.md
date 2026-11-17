---
id: engineering-technology.aerospace-engineering.orbital-mechanics.walker-constellation-design
name: walker-constellation-design
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, constellation-design, constellations, coverage, walker, walker-delta, phasing-factor, navigation-constellation]
level: practitioner
status: verified
description: "Design Walker delta constellations in i:T/P/F notation, choose planes, phasing and altitude for coverage, and check minimum elevation and revisit."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Walker, Circular orbit patterns providing continuous whole earth coverage"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "GPS.gov space segment, https://www.gps.gov/space-segment"
  - "ESA Navipedia Galileo Space Segment, https://gssc.esa.int/navipedia/index.php/Galileo_Space_Segment"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Walker constellation design

**Goal:** a symmetric set of satellites providing the required coverage.

## Notation
Walker delta pattern `i: T/P/F`: inclination `i`, total satellites `T`, equally spaced planes `P`, relative phasing factor `F` (0 to `P - 1`). Planes are spaced `360/P` degrees apart in RAAN; satellites in adjacent planes are phased by `F * 360/T` degrees. GPS has a baseline of 24 slots in 6 equally spaced planes at 55 degrees (gps.gov, NASA); Galileo is Walker 24/3/1 at 56 degrees nominal with 8 active satellites and a spare per plane (ESA Navipedia).

## Design steps
1. Define coverage: global vs regional, minimum elevation angle, number of satellites in view required.
2. Pick altitude (from link budget, radiation environment, delta-v, drag).
3. Pick `i` to match the latitude band of interest (higher inclination covers poles; near-equatorial favours low latitudes).
4. Search `T/P/F` with a coverage simulation (grid of ground points, propagate over a repeat period) measuring minimum satellites in view and maximum gap.
5. Check robustness to a failed satellite and station-keeping demand.

## Gotchas
- Phasing factor affects collision geometry at plane crossings; choose `F` so satellites do not meet at the nodes.
- Perturbations (J2) drift planes differentially if altitudes differ; maintain altitude control.

## Verify
- [ ] Coverage simulation shows minimum satellites in view above the requirement at all grid points.
