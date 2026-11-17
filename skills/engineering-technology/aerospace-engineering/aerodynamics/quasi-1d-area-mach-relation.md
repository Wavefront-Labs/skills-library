---
id: engineering-technology.aerospace-engineering.aerodynamics.quasi-1d-area-mach-relation
name: quasi-1d-area-mach-relation
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [area-mach-relation, compressible-flow, isentropic-flow, choked-flow, nozzle-flow, gas-dynamics]
level: practitioner
status: verified
description: "Use the isentropic area-Mach relation to size ducts and nozzles, find subsonic and supersonic Mach for an area ratio, and compute choked mass flow."
sources:
  - "Anderson, Fundamentals of Aerodynamics"
  - "Mattingly, Elements of Propulsion"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Quasi-1D area-Mach relation

**Goal:** relate local area to Mach number for steady, isentropic, adiabatic flow of a calorically perfect gas.

## Relations
- `A/A* = (1/M) * [ (2/(gamma+1)) * (1 + (gamma-1)/2 * M^2) ]^((gamma+1)/(2(gamma-1)))`. For `gamma = 1.4` the exponent is 3.
- `A*` is the area where `M = 1`, real or imaginary; it is a reference, not necessarily a physical throat.
- Choked mass flow: `mdot = A * pt * sqrt(gamma/(R*Tt)) * M * (1 + (gamma-1)/2 * M^2)^(-(gamma+1)/(2(gamma-1)))`, maximal at `M = 1`. For air in SI units `mdot*sqrt(Tt)/(A*pt)` is about 0.0404 at `M = 1`.

## Procedure
1. Compute `A/A*` from the geometry (throat or sonic area as `A*`).
2. Solve for `M` numerically (bisection or `fzero`). Every `A/A* > 1` has two roots: pick the subsonic root upstream of the throat, and the supersonic root downstream only if the back pressure allows it.
3. Get `p/pt`, `T/Tt` from `(1 + (gamma-1)/2 M^2)^(-gamma/(gamma-1))` and `^(-1)`.
4. If a normal shock sits in the divergent section, `A*` changes across it; use `pt` after the shock (see normal-shock-relations).

## Worked checks (gamma 1.4)
`M = 2` gives `A/A* = 1.688`; `M = 0.5` gives `A/A* = 1.340`.

## Gotchas
- Friction, heat addition and area change together are not isentropic; this relation then fails.
- Boundary-layer blockage makes the effective throat smaller than the geometric one.
- Do not pick the wrong root: a supersonic exit needs the supersonic solution.

## Verify
- [ ] The computed `M` reproduces the original `A/A*` when substituted back.
