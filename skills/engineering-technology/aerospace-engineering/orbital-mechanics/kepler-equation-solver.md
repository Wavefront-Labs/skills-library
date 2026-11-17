---
id: engineering-technology.aerospace-engineering.orbital-mechanics.kepler-equation-solver
name: kepler-equation-solver
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, two-body, keplerian-orbits, kepler-equation, mean-anomaly, eccentric-anomaly, true-anomaly, newton-raphson]
level: practitioner
status: verified
description: "Solve Kepler's equation for elliptic and hyperbolic orbits robustly with Newton iteration, choose good starting values, and convert to true anomaly."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Battin, An Introduction to the Mathematics and Methods of Astrodynamics"
  - "Recomputed in Python (Newton iteration residuals)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Kepler equation solver

**Goal:** position on an orbit at a given time.

## Elliptic orbits (`e < 1`)
- Mean anomaly `M = n (t - t_p)`, `n = sqrt(mu/a^3)`.
- Kepler: `M = E - e sin(E)`; solve for `E` with Newton: `E_{k+1} = E_k - (E_k - e sin E_k - M)/(1 - e cos E_k)`.
- Start: `E0 = M` for `e < 0.8`; `E0 = pi` for higher eccentricity (more robust). Wrap `M` into `[-pi, pi]` first. Converge to about 1e-12 (checked: Newton from E0 = pi at e = 0.9 and 0.99, and from E0 = M at e = 0.1, reaches residual below 1e-15 within 50 iterations for M = 1 rad).
- True anomaly: `tan(nu/2) = sqrt((1+e)/(1-e)) tan(E/2)` (use `atan2` to get the correct quadrant); radius `r = a (1 - e cos E)`.

## Hyperbolic (`e > 1`)
`M_h = e sinh(F) - F`, Newton on `F`; `tan(nu/2) = sqrt((e+1)/(e-1)) tanh(F/2)`.

## Parabolic and near-parabolic
Use the universal-variable formulation (Stumpff functions) to avoid singularities.

## Practice
1. Use `mu_Earth = 398600.4418 km^3/s^2` and consistent units.
2. Guard against `e` near 1 (slow convergence): use a bracketed solver or a higher-order method (Halley, Danby).
3. Propagate the state in the perifocal frame, then rotate to inertial with the orbital elements.

## Verify
- [ ] Round trip `M -> E -> M` closes to 1e-12.
- [ ] A circular orbit (`e = 0`) returns `E = M`.
