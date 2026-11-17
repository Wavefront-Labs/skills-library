---
id: engineering-technology.aerospace-engineering.orbital-mechanics.phasing-orbit-design
name: phasing-orbit-design
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [phasing, phasing-orbit, rendezvous, catch-up, orbit-transfers, launch-and-rendezvous]
level: practitioner
status: verified
description: "Design a coplanar phasing orbit to close an angular phase offset between two spacecraft in a chosen number of revolutions, with the burn and perigee checks."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Recomputed in Python"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Phasing orbits

**Goal:** change the in-track separation of a chaser relative to a target in the same circular orbit.

## Method
1. Let `T` be the target (and initial chaser) period and `dtheta` the phase angle the chaser must gain (positive when it must catch up).
2. For `k` revolutions of the phasing orbit: `T_ph = T * (1 - dtheta/(2 pi k))`. Use `1 + ...` if the chaser must lose phase.
3. Phasing orbit semi-major axis `a_ph = (mu (T_ph/(2 pi))^2)^(1/3)`.
4. Burn at the burn point (the radius `r`, shared with the original circular orbit): `v_ph = sqrt(mu (2/r - 1/a_ph))`, `dv = v_ph - sqrt(mu/r)`. After `k` revolutions burn again by `-dv` to recircularise.
5. A catch-up uses a lower orbit (shorter period): the burn is retrograde at the original apoapsis point; a lose-phase manoeuvre uses a higher orbit.

## Checks
- Worked check (computed): 500 km circular, gain 30 degrees in 3 revolutions gives `a_ph` = 6750.17 km, `dv` = -72.5 m/s, perigee altitude 244 km; period of the phasing orbit matches `T_ph` to 1e-12 s.
- Perigee radius of the phasing orbit above the atmosphere and above any other constraint (for a catch-up orbit, `r_p = 2 a_ph - r` ).
- Total delta-v `2 |dv|` and the number of revolutions trade: more revolutions mean smaller delta-v and longer time.

## Gotchas
- Differential drag, J2 and eccentricity change the phasing in practice; plan a correction burn.
- Rendezvous safety requires approach corridors and abort rules beyond this geometry.

## Verify
- [ ] Propagating the two spacecraft shows the phase offset closing to zero after `k` revolutions.
