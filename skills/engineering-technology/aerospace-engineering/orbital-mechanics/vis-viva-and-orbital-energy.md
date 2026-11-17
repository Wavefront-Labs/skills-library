---
id: engineering-technology.aerospace-engineering.orbital-mechanics.vis-viva-and-orbital-energy
name: vis-viva-and-orbital-energy
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [vis-viva, orbital-energy, escape-velocity, circular-velocity, orbit-period, two-body-motion]
level: practitioner
status: verified
description: "Use the vis-viva equation and specific orbital energy to get speed at any radius, period, escape speed and burn effects for two-body orbits."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "NASA Earth Fact Sheet, https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Vis-viva and energy

**Goal:** speeds, periods and energy changes from `a` and `r`.

## Equations
- `v^2 = mu * (2/r - 1/a)` (vis-viva). Circular: `v = sqrt(mu/r)`. Escape at `r`: `sqrt(2 mu/r)`.
- Specific energy `eps = v^2/2 - mu/r = -mu/(2a)`. Negative for bound orbits, zero for parabolic, positive for hyperbolic.
- Period `T = 2 pi sqrt(a^3/mu)`; mean motion `n = sqrt(mu/a^3)`.
- Periapsis and apoapsis radii `rp = a(1-e)`, `ra = a(1+e)`; `v_p = sqrt(mu (1+e)/ (a(1-e)))`.

## Uses
1. Burn effect: an in-track burn `dv` at radius `r` gives `eps_new = eps + v dv` (for small `dv`), so prograde burns near periapsis raise the energy most per unit `dv` (the Oberth effect).
2. Hyperbolic excess speed: `v_inf^2 = 2 eps`; launch energy `C3 = v_inf^2`.
3. Transfer orbits (see hohmann-transfer): `a_t = (r1 + r2)/2` then speeds from vis-viva.

## Examples
Circular speed at 400 km altitude is about 7.67 km/s; escape from there about 10.84 km/s; LEO period about 92.6 minutes (computed with mu = 398600.4418 km^3/s^2, R = 6378.137 km).

## Gotchas
- `r` is measured from the centre of the body.
- Vis-viva gives speed only, not direction: use the flight path angle for the velocity vector.

## Verify
- [ ] Speed at periapsis from vis-viva equals the one from angular momentum `h/r_p`.
