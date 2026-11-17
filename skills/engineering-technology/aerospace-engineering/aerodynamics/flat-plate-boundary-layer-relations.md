---
id: engineering-technology.aerospace-engineering.aerodynamics.flat-plate-boundary-layer-relations
name: flat-plate-boundary-layer-relations
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, boundary-layer, viscous-flow, flat-plate-boundary-layer, blasius, skin-friction, displacement-thickness, momentum-thickness]
level: practitioner
status: verified
description: "Use the classic laminar and turbulent flat-plate boundary-layer formulas for thickness, skin friction and drag, with the transition estimate and their validity limits."
sources:
  - "White, Viscous Fluid Flow"
  - "Schlichting and Gersten, Boundary-Layer Theory"
  - "Anderson, Fundamentals of Aerodynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Flat-plate boundary-layer relations

**Goal:** quick estimates of boundary-layer thickness and friction drag.

## Laminar (Blasius)
- `delta_99 = 4.91 x / sqrt(Re_x)` (Blasius solution; 5.0 is the usual rounded textbook value)
- `Cf = 0.664 / sqrt(Re_x)`; plate drag coefficient `CD = 1.328 / sqrt(Re_L)`.
- Displacement thickness `delta* = 1.72 x / sqrt(Re_x)`; momentum thickness `theta = 0.664 x / sqrt(Re_x)`.

## Turbulent (power-law approximations)
The constants below (0.37, 0.0592, 0.074, 0.455 and the validity range) are textbook fits (gated: unconfirmed, source is paywalled or blocked).
- `delta = 0.37 x / Re_x^0.2`
- `Cf = 0.0592 / Re_x^0.2`, `CD = 0.074 / Re_L^0.2` (valid roughly 5e5 < Re < 1e7).
- For higher Re use the Schlichting log-law fit `Cf = 0.455 / (log10 Re)^2.58`.
- Shape factor `H = delta*/theta` is 2.59 laminar (Blasius); about 1.3-1.4 turbulent (gated: unconfirmed, source is paywalled or blocked).

## Transition
Natural transition on a smooth flat plate in low turbulence occurs at about `Re_x` of 3e5 to 5e5; free-stream turbulence, roughness and pressure gradient shift it. Mixed laminar-turbulent drag: subtract the turbulent drag over the laminar length and add the laminar value (the "transition correction").

## Gotchas
- Compressibility reduces Cf (use Van Driest or reference temperature methods above Mach 1).
- Pressure gradients (airfoil) alter shape factors and separation; use integral methods or CFD.
- Use the local Reynolds number based on the surface running length, not the freestream-based length.

## Verify
- [ ] Re_x = 1e6: laminar delta = 4.91e-3 x (5.0e-3 rounded); turbulent delta = 0.37 x / 15.8 = 0.0234 x.
- [ ] Your plate drag decreases with Re at the stated exponent.
