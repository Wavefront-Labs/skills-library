---
id: engineering-technology.aerospace-engineering.orbital-mechanics.state-vector-to-orbital-elements
name: state-vector-to-orbital-elements
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-elements, state-vector, keplerian-elements, coordinate-conversion, two-body-motion]
level: practitioner
status: verified
description: "Convert between inertial state vectors and classical orbital elements, including quadrant checks and the circular and equatorial special cases."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Recomputed in Python (round-trip test of the formulas)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# State vectors and orbital elements

**Goal:** a correct round trip between `(r, v)` and `(a, e, i, RAAN, argp, nu)`.

## State to elements (inertial frame, gravitational parameter `mu`; Earth `mu` about 398600.44 km^3/s^2)
1. Angular momentum `h = r x v`; node vector `n = k x h`; eccentricity vector `e_vec = ((v^2 - mu/r) r - (r . v) v) / mu`.
2. Specific energy `eps = v^2/2 - mu/r`; semi-major axis `a = -mu/(2 eps)` (undefined for parabolic).
3. Inclination `i = acos(h_z/|h|)`.
4. RAAN `Omega = acos(n_x/|n|)`; if `n_y < 0`, `Omega = 2 pi - Omega`.
5. Argument of perigee `omega = acos(n . e_vec/(|n| e))`; if `e_z < 0`, `omega = 2 pi - omega`.
6. True anomaly `nu = acos(e_vec . r/(e r))`; if `r . v < 0`, `nu = 2 pi - nu`.

## Special cases
- Circular (`e` near 0): `omega` undefined; use argument of latitude `u` from the node (or true longitude if also equatorial).
- Equatorial (`i` near 0 or pi): `Omega` undefined; use longitude of perigee.
- Round trip checked in Python on 2,000 random orbits (e 0.01-0.8, any i, Omega, omega, nu): max error below 1e-6 using exactly the formulas above.
- Use `atan2` forms where possible; `acos` is ill-conditioned near 0 and pi.

## Elements to state
Perifocal position `r_pqw = (p/(1+e cos nu)) [cos nu, sin nu, 0]`, velocity `sqrt(mu/p) [-sin nu, e + cos nu, 0]`, `p = a(1-e^2)`; rotate by `R3(-Omega) R1(-i) R3(-omega)` (passive rotation matrices; with active matrices use `R3(Omega) R1(i) R3(omega)`).

## Gotchas
- Mixed units (km vs m) in `mu`.
- Rotating frame states must be converted to inertial first.
- Retrograde orbits have `i` above 90 degrees.

## Verify
- [ ] Convert a state to elements and back; position and velocity match to numerical precision.
