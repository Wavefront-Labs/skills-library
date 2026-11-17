---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.spatial-schemes-and-limiters
name: spatial-schemes-and-limiters
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, numerical-methods, discretisation, numerical-schemes, flux-limiters, muscl, roe-flux, ausm, upwind, venkatakrishnan]
level: advanced
status: draft
description: "Select spatial discretisation: first vs second-order upwind, MUSCL with limiters, and Roe or AUSM fluxes, with the stability and accuracy trade-offs."
sources:
  - "Blazek, Computational Fluid Dynamics Principles and Applications"
  - "Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics"
  - "Solver theory guides"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Spatial schemes and limiters

**Goal:** accuracy without oscillations at shocks.

## Choices
- **First-order upwind:** robust, very diffusive; use for starting and for rough convergence, not for results.
- **Second-order upwind / MUSCL:** reconstruct left/right states with gradients (Green-Gauss or least squares) and limit them.
- **Limiters:** minmod (most dissipative), van Leer, van Albada, Venkatakrishnan (smooth, aids convergence on unstructured grids but can stall convergence), Barth-Jespersen (strict). Limiters trade monotonicity against residual convergence.
- **Flux functions:** Roe flux-difference splitting (accurate for boundary layers, can need an entropy fix and shows carbuncle instability on some grids); AUSM family (robust at strong shocks); HLLC (robust, preserves contacts); central with artificial dissipation (JST) in structured codes.

## Practice
1. Start first-order to initialise, then switch to second-order.
2. Use a limiter freeze after initial convergence if residuals stall.
3. For hypersonic strong shocks pick AUSM or HLLC with a smooth limiter; for transonic cruise, Roe with Venkatakrishnan is typical.
4. Check dissipation sensitivity by comparing two schemes on the same mesh.

## Gotchas
- Gradient method matters on skewed meshes: least squares is usually more robust than Green-Gauss node-based.
- Limiter clipping near smooth extrema reduces order.

## Verify
- [ ] Forces at second-order differ from first-order by a plausible, documented amount.
- [ ] No overshoots or non-physical pressure oscillations at shocks.
