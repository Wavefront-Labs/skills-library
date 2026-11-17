---
id: engineering-technology.aerospace-engineering.aerodynamics.normal-shock-relations
name: normal-shock-relations
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, compressible-flow, gas-dynamics, normal-shock, shock-relations, stagnation-pressure-loss, rayleigh-pitot, pitot]
level: practitioner
status: verified
description: "Compute normal-shock jump conditions and stagnation-pressure loss for a perfect gas, with a worked M=2 check and the Rayleigh pitot relation."
sources:
  - "Anderson, Modern Compressible Flow"
  - "Liepmann and Roshko, Elements of Gasdynamics"
  - "NACA Report 1135 (Ames Research Staff)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Normal shock relations (perfect gas, gamma = 1.4)

**Goal:** conditions behind a normal shock from the upstream Mach number `M1`.

## Relations
- `p2/p1 = 1 + 2 gamma/(gamma+1) (M1^2 - 1)`
- `rho2/rho1 = (gamma+1) M1^2 / ((gamma-1) M1^2 + 2)`
- `M2^2 = (1 + (gamma-1)/2 M1^2) / (gamma M1^2 - (gamma-1)/2)`
- `T2/T1 = (p2/p1)(rho1/rho2)`; stagnation temperature is conserved, stagnation pressure drops: `p02/p01 < 1`.

## Check: M1 = 2
`p2/p1 = 4.5`, `rho2/rho1 = 2.667`, `T2/T1 = 1.687`, `M2 = 0.577`, `p02/p01 = 0.721`.

## Pitot in supersonic flow
A pitot probe behind a detached bow shock reads `p02`; use the Rayleigh pitot formula `p02/p1 = [(gamma+1)M1^2/2]^(gamma/(gamma-1)) / [(2 gamma M1^2 - (gamma-1))/(gamma+1)]^(1/(gamma-1))` to get `M1` from `p02/p1`.

## Applications
- Inlet design: shock losses set pressure recovery (see inlet skills).
- Wind-tunnel diffusers and starting problems.
- Intuition for wave drag: entropy rise implies a loss.

## Gotchas
- Perfect-gas formulas break down at high temperatures (vibrational excitation, dissociation) above about M 5.
- Use total (stagnation) quantities consistently; units and reference states matter.

## Verify
- [ ] M1 = 1 returns unity ratios.
- [ ] M1 = 2 matches the numbers above to three digits.
