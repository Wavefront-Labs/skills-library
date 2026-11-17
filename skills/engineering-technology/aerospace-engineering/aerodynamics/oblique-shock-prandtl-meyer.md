---
id: engineering-technology.aerospace-engineering.aerodynamics.oblique-shock-prandtl-meyer
name: oblique-shock-prandtl-meyer
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, compressible-flow, gas-dynamics, oblique-shock, prandtl-meyer, theta-beta-mach, expansion-fan, shock-expansion-theory]
level: practitioner
status: verified
description: "Solve oblique-shock theta-beta-Mach problems and Prandtl-Meyer expansions for supersonic flow over wedges, corners and thin airfoils."
sources:
  - "Anderson, Modern Compressible Flow"
  - "Liepmann and Roshko, Elements of Gasdynamics"
  - "NACA Report 1135"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Oblique shocks and Prandtl-Meyer expansion

**Goal:** flow properties after turning supersonic flow through a compression corner or expansion corner.

## Oblique shock
- Relation: `tan(theta) = 2 cot(beta) (M1^2 sin^2(beta) - 1) / (M1^2 (gamma + cos(2 beta)) + 2)`
- Normal component: `M_n1 = M1 sin(beta)`; use the normal-shock formulas with `M_n1`, then `M2 = M_n2 / sin(beta - theta)`.
- For a given `M1` and `theta` there are two solutions (weak and strong) up to a maximum deflection (about 23 degrees at M1 = 2, gamma 1.4); beyond it the shock detaches. The weak solution is the usual one.

## Prandtl-Meyer expansion (isentropic)
`nu(M) = sqrt((gamma+1)/(gamma-1)) atan( sqrt((gamma-1)/(gamma+1) (M^2-1)) ) - atan( sqrt(M^2-1) )`
`nu(2) = 26.38 degrees`. For a turn of `theta`, `nu(M2) = nu(M1) + theta`; solve for `M2` by inversion (Newton or tables).

## Uses
- Shock-expansion theory: supersonic diamond or flat-plate airfoil pressure distribution and wave drag per unit span.
- Linear (Ackeret) check: `Cp = 2 theta / sqrt(M^2 - 1)`.
- Inlet ramp design and nozzle contour reasoning.

## Gotchas
- Solve with a bracketed root-finder; the beta equation has multiple roots.
- Expansions are isentropic; shocks are not. Do not combine entropy-changing and isentropic steps carelessly when computing total pressure.

## Verify
- [ ] Zero turning angle returns a Mach wave, `beta = asin(1/M1)`.
- [ ] Shock followed by equal expansion does not return the original pressure (entropy rose); confirm in your code.
