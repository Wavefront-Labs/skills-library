---
id: engineering-technology.aerospace-engineering.orbital-mechanics.jacobi-constant-and-zero-velocity-curves
name: jacobi-constant-and-zero-velocity-curves
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [jacobi-constant, zero-velocity-curves, crtbp, hill-region, three-body-dynamics, energy-accessibility]
level: practitioner
status: verified
description: "Compute the Jacobi constant and zero-velocity curves in the restricted three-body problem to decide which regions a trajectory can reach."
sources:
  - "Koon, Lo, Marsden and Ross, Dynamical Systems, the Three-Body Problem and Space Mission Design"
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Recomputed in Python (2U at each libration point)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Jacobi constant

**Goal:** the integral of motion for the CRTBP and what it says about reachable space.

## Definition (rotating frame, non-dimensional units)
`C = 2 U - (vx^2 + vy^2 + vz^2)`, with `U = (x^2 + y^2)/2 + (1-mu)/r1 + mu/r2`. Larger `C` means lower energy.
- Zero-velocity surface: `2U(x,y,z) = C`; the spacecraft cannot cross to the region where `2U < C`.

## Use
1. Compute `C` for the initial state.
2. Compare with the Jacobi constants at the libration points `C_L1 > C_L2 > C_L3 > C_L4 = C_L5`, where `C_L4 = C_L5 = 3 - mu(1 - mu)` (tends to 3 as mu -> 0). Computed for the Earth-Moon system (mu = 0.012150585): `C_L1` = 3.188, `C_L2` = 3.172, `C_L3` = 3.012, `C_L4` = `C_L5` = 2.988.
3. If `C > C_L1`, the neck at L1 is closed: the orbit stays near Earth or the Moon. If `C` is between `C_L1` and `C_L2`, the L1 neck is open; between `C_L2` and `C_L3`, the L2 neck opens too. Transfers designed with low-energy gateways use these openings.
4. Plot zero-velocity curves in the `x-y` plane to see the allowed region.
5. Verify integration accuracy by monitoring `C` over time.

## Gotchas
- `C` is constant only in the CRTBP; with ephemeris perturbations it changes and is used as a diagnostic only.
- Do not confuse `C` with `C3`.

## Verify
- [ ] `C` drifts less than 1e-10 over a propagation with tight tolerances.
