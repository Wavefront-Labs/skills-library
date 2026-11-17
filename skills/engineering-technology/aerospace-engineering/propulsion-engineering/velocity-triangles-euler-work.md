---
id: engineering-technology.aerospace-engineering.propulsion-engineering.velocity-triangles-euler-work
name: velocity-triangles-euler-work
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, turbomachinery, compressors, velocity-triangles, euler-work, stage-loading, degree-of-reaction, diffusion-factor]
level: practitioner
status: gated
description: "Draw and compute axial compressor and turbine velocity triangles, apply the Euler work equation, and check loading, reaction and diffusion factor limits."
sources:
  - "Dixon and Hall, Fluid Mechanics and Thermodynamics of Turbomachinery"
  - "Mattingly, Elements of Propulsion"
  - "Saravanamuttoo et al., Gas Turbine Theory"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Velocity triangles and Euler work

**Goal:** stage-level aerodynamic design check.

## Definitions
Absolute velocity `C`, blade speed `U`, relative velocity `W = C - U` (vector). Axial component `C_a`; swirl component `C_theta`. Flow coefficient `phi = C_a/U`; loading coefficient `psi = Delta h0/U^2`.

## Euler work equation
`w = Delta h0 = U2 C_theta2 - U1 C_theta1`; for an axial stage with constant `U`: `w = U (C_theta2 - C_theta1)`. Stage temperature rise `Delta T0 = w/cp`.

## Degree of reaction
`R = (static enthalpy rise in rotor)/(stage static enthalpy rise)`; 50% reaction gives symmetric triangles, commonly used in compressors.

## Diffusion limits
- De Haller number `W2/W1 >= 0.72` as a rule of thumb for blade rows (gated: unconfirmed, source is paywalled or blocked).
- Lieblein diffusion factor `D = 1 - W2/W1 + Delta C_theta/(2 sigma W1)` limit about 0.6 (solidity `sigma`) (gated: unconfirmed, source is paywalled or blocked).
- Tip Mach number limits (relative Mach at the tip about 1.2-1.6 for transonic fans, depending on design (gated: unconfirmed, source is paywalled or blocked)).

## Procedure
1. Choose `U`, `C_a`, and `psi`; set inlet swirl (zero for first rotor).
2. Construct triangles at mean radius (and at hub and tip with radial equilibrium for realistic twist).
3. Compute work, temperature rise and pressure rise using stage efficiency.
4. Check D, de Haller and Mach limits; adjust.

## Verify
- [ ] Work calculated from triangles equals `cp Delta T0` from stagnation temperatures.
- Worked check (computed): U = 300 m/s, C_a = 150 m/s, zero inlet swirl, C_theta2 = 100 m/s gives w = 30 kJ/kg, Delta T0 = 29.9 K (cp 1005), phi = 0.5, psi = 0.333, W2/W1 = 0.745, D = 0.40 at solidity 1.
