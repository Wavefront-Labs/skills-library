---
id: engineering-technology.aerospace-engineering.orbital-mechanics.third-body-and-solar-radiation-pressure
name: third-body-and-solar-radiation-pressure
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [third-body, solar-radiation-pressure, srp, lunisolar-perturbation, geo-inclination-drift, orbital-perturbations]
level: practitioner
status: gated
description: "Model third-body (Sun, Moon) and solar radiation pressure accelerations and their effects on GEO inclination, eccentricity and station keeping."
sources:
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Montenbruck and Gill, Satellite Orbits"
  - "Soop, Handbook of Geostationary Orbits"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Third body and radiation pressure

**Goal:** the perturbations that dominate high orbits.

## Third-body acceleration
`a = mu_3 * ( (r_3 - r)/|r_3 - r|^3 - r_3/|r_3|^3 )`, where `r_3` is the third body position from the central body. The second term is the indirect part.
- Needs Sun and Moon ephemerides (for example JPL DE kernels via SPICE).

## Solar radiation pressure
- `a = -P * Cr * (A/m) * s_hat` with `P` = S/c about 4.54e-6 N/m^2 at 1 AU for S = 1361 W/m^2 (4.56e-6 corresponds to the older 1367 W/m^2; computed), `s_hat` the unit vector from the Sun to the spacecraft, `Cr` between 1 (absorbing) and 2 (specular), an assumed coefficient.
- Include shadow (cylindrical or conical umbra and penumbra) for eclipse periods.
- Area-to-mass ratio drives the size; large light structures (arrays, sails) are sensitive.

## Effects at GEO
- Lunisolar attraction drives the orbit-normal drift, raising inclination at an average of about 0.75 to 0.95 degrees per year; north-south station keeping typically costs about 45 to 50 m/s per year (both ranges (gated: unconfirmed, source is paywalled or blocked)).
- SRP drives eccentricity; east-west drift comes from the tesseral gravity harmonics.

## Procedure
1. Include both effects in numerical propagation (see numerical-orbit-propagation).
2. Estimate `Cr` from spacecraft geometry or from tracking data.
3. Evaluate the delta-v budget for station keeping and momentum unloading.

## Gotchas
- Using body-fixed vs inertial position for the Moon introduces errors.
- Cr varies with attitude and degrades with time.
- Estimating `Cr` from orbit data absorbs unmodelled accelerations.

## Verify
- [ ] The computed GEO inclination drift is within the known 0.75 to 0.95 degrees per year range.
