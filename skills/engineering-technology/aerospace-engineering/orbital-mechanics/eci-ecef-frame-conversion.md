---
id: engineering-technology.aerospace-engineering.orbital-mechanics.eci-ecef-frame-conversion
name: eci-ecef-frame-conversion
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [eci-ecef, reference-frames, gcrf, itrf, sidereal-time, teme]
level: practitioner
status: gated
description: "Convert between ECI and ECEF with Earth rotation angle, and know when precession, nutation and polar motion corrections matter."
sources:
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "IERS Conventions"
  - "IAU SOFA documentation"
  - "IAU SOFA, http://www.iausofa.org/"
  - "Recomputed in Python (error magnitude)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ECI and ECEF frames

**Goal:** a correct rotation between inertial and Earth-fixed coordinates.

## Simple rotation (accuracy of kilometres or less)
`r_ECEF = R3(theta) r_ECI`, with `theta` the Greenwich sidereal angle: `theta(t) = theta0 + omega_E (t - t0)`, `omega_E = 7.292115e-5 rad/s`. Fine for ground track plots and coarse visibility.

## Full chain (metre-level or better)
`r_ITRF = W(t) R(t) N(t) P(t) r_GCRF` where:
- `P`, `N`: precession and nutation (IAU 2006/2000A models) (gated: unconfirmed, the SOFA site fetched did not list routines).
- `R`: Earth rotation using UT1 (needs UT1 minus UTC from IERS bulletins).
- `W`: polar motion from IERS data.
Use a tested library (IAU SOFA routines, which the IAU provides free in Fortran 77 and ANSI C; Astropy, Orekit, MATLAB Aerospace Toolbox functions for ECI and ECEF conversion) rather than hand-coding.

## Frames to distinguish
- **GCRF/J2000**: inertial frame for precise work.
- **TEME**: the true-equator mean-equinox frame in which SGP4 outputs are expressed (gated: unconfirmed, the Spacetrack Report PDF could not be read; see tle-and-sgp4-propagation); convert it before comparing to other sources.
- **ITRF**: Earth-fixed.

## Procedure
1. Fix the time scales: UTC to UT1, TT/TDB for ephemerides; apply leap seconds correctly.
2. Pick the frame chain for the required accuracy.
3. Convert velocity with the transport term: `v_ECEF = R (v_ECI - omega_E x r_ECI)`.

## Gotchas
- Using UTC for the rotation angle gives errors up to ~0.9 s of Earth rotation (about 419 m at the equator, computed from 0.9 s x 7.292115e-5 rad/s x 6378.137 km).
- Position-only conversions miss the `omega x r` term in velocity.
- Different libraries use different sign or ordering conventions for rotations; test with a known point.

## Verify
- [ ] A point on the Earth's surface converted ECEF to ECI and back returns the original coordinates.
