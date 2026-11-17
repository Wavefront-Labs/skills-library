---
id: engineering-technology.aerospace-engineering.orbital-mechanics.launch-azimuth-and-inclination
name: launch-azimuth-and-inclination
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, launch-and-rendezvous, launch-windows, rendezvous, launch-azimuth, inclination, earth-rotation, launch-site]
level: practitioner
status: verified
description: "Compute launch azimuth for a target inclination from a launch site latitude, include Earth rotation, and understand achievable inclinations and range limits."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Launch vehicle user guides"
  - "NASA Earth Fact Sheet, https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html"
  - "Recomputed in Python (v_rot; example 28.5 deg site to 51.6 deg: inertial azimuth 44.98, compensated 42.74 degrees)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Launch azimuth and inclination

**Goal:** heading needed to reach a target inclination from a given site.

## Relations
- Inertial azimuth: `sin(Az_i) = cos(i) / cos(phi)` for site latitude `phi`; direct ascent needs `i >= |phi|`.
- Earth rotation adds eastward velocity `v_rot = 0.4651 cos(phi)` km/s (2 pi R/T_sidereal with R = 6378.137 km, T = 86164.1 s gives 0.4651 km/s); compensated azimuth: `tan(Az) = (v_orb sin(Az_i) - v_rot) / (v_orb cos(Az_i))` (with `v_orb` about 7.7 km/s in LEO).
- Launching due east (`Az = 90 degrees`) from latitude `phi` gives inclination `i = phi`, the most efficient for that site.

## Planning
1. Compute both ascending (northeast) and descending (southeast) azimuths.
2. Check range safety azimuth limits for the launch range (over-water corridors); sites choose launch ranges to protect populated areas.
3. Dog-leg manoeuvres reach lower inclinations than the site latitude but cost delta-v.
4. Launch window: for a given orbital plane the site passes through the plane twice daily; for rendezvous the target's plane sets the window.

## Gotchas
- Higher inclinations from low latitudes lose the rotation benefit.
- Sun-synchronous launches are retrograde (inclination above 90 degrees) and fly with southerly azimuths.

## Verify
- [ ] Equatorial site: `Az_i = 90 degrees` for `i = 0`; high latitude site returns an error when `i < |phi|`.
