---
id: engineering-technology.aerospace-engineering.orbital-mechanics.ground-track-computation
name: ground-track-computation
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [ground-track, sub-satellite-point, earth-rotation, coverage, constellation-design]
level: practitioner
status: verified
description: "Compute a satellite ground track from orbital elements, including Earth rotation, nodal regression and the shift per orbit."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "NASA Earth Fact Sheet, https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html (sidereal day 23.9345 h)"
  - "Recomputed in Python"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ground tracks

**Goal:** the latitude and longitude of the point below the satellite over time.

## Method
1. Propagate to get the inertial position `r_ECI(t)` (see numerical-orbit-propagation or Kepler propagation).
2. Convert to Earth-fixed coordinates with the sidereal rotation angle (see eci-ecef-frame-conversion).
3. Latitude `phi = asin(z/r)` (geocentric; convert to geodetic if needed); longitude `lambda = atan2(y, x)` from the Earth-fixed position.
4. Plot over the interval.

## Properties
- Maximum latitude equals the inclination (or `180 - i` for retrograde orbits).
- The track shifts westward each orbit by about `omega_E * T_nodal` (Earth rotates about 360.9856 degrees per solar day, rate `7.292115e-5 rad/s`). For a 90-minute orbit the shift is about 22.6 degrees (360.9856/1440 x 90 = 22.56, computed).
- J2 nodal regression changes the node rate (see j2-secular-effects) and thus the shift.

## Uses
Coverage analysis, ground station visibility, sun-synchronous revisit (see sun-synchronous-orbit-design), repeat tracks (see repeat-ground-track-design).

## Gotchas
- Use the correct sidereal time (UT1) for the rotation angle.
- Geodetic vs geocentric latitude differ by up to about 0.192 degrees (computed with WGS84 flattening 1/298.257223563, maximum near 45 degrees).
- Wrap the longitude at plus or minus 180 degrees when plotting to avoid false lines.

## Verify
- [ ] The computed shift per orbit matches `omega_E T` within a small J2 correction.
