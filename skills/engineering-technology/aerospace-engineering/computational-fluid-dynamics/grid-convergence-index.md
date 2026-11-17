---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.grid-convergence-index
name: grid-convergence-index
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, meshing, mesh-generation, grid-convergence-index, gci, richardson-extrapolation, grid-refinement, discretisation-error, roache]
level: advanced
status: gated
description: "Quantify discretisation error with three systematically refined grids using Richardson extrapolation and the Roache grid convergence index."
sources:
  - "Roache, Verification and Validation in Computational Science and Engineering"
  - "Celik et al., Procedure for estimation of uncertainty due to discretization (ASME Journal of Fluids Engineering 2008)"
  - "ASME V&V 20"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Grid convergence index (GCI)

**Goal:** an uncertainty estimate for a quantity of interest (drag, lift, peak pressure).

## Procedure (three grids, constant refinement ratio r)
1. Build coarse, medium and fine grids with `r` of at least about 1.3 (Celik et al. recommend about 1.3 (gated: unconfirmed, source is paywalled or blocked); the NASA Glenn validation page says r >= 1.1 minimum) (refine in all directions; keep the mesh topology and layer structure the same).
2. Solve all three to the same iterative convergence; record `f1` (fine), `f2` (medium), `f3` (coarse).
3. Apparent order: `p = ln( (f3 - f2) / (f2 - f1) ) / ln(r)` (for monotone convergence).
4. Richardson extrapolation: `f_exact ~ f1 + (f1 - f2) / (r^p - 1)`.
5. GCI on the fine grid: `GCI = Fs * |(f2 - f1)/f1| / (r^p - 1)` with safety factor `Fs = 1.25` for three or more grids (3.0 for two grids), as on the NASA Glenn validation page (https://www.grc.nasa.gov/WWW/wind/valid/tutorial/spatconv.html), whose worked example (p = 1.786, GCI 0.103%) matches these formulas. Check asymptotic range with GCI23 about r^p GCI12.

## Checks
- Monotone convergence: `(f3-f2)` and `(f2-f1)` the same sign. Oscillating convergence needs more grids.
- The observed `p` should be near the formal order of the scheme (about 2 for second-order); large differences indicate the grids are not in the asymptotic range, or shocks and limiters are lowering order.

## Gotchas
- Unstructured grids with non-uniform refinement make `r` ambiguous: use `r = (N_fine/N_coarse)^(1/dim)` per Celik (gated: unconfirmed, source is paywalled or blocked), or use a structured family.
- Report the quantity and grid sizes along with GCI.

## Verify
- [ ] Monotone convergence, `p` in a plausible range, and GCI below the target tolerance.
