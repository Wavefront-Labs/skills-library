---
id: engineering-technology.aerospace-engineering.matlab-simulink.extract-stability-derivatives-from-linear-model
name: extract-stability-derivatives-from-linear-model
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [derivative-extraction, stability-derivatives, linearization, finite-difference, state-space]
level: practitioner
status: docs-checked
description: "Pull dimensional stability derivatives out of a trimmed nonlinear simulation by linearisation or central differences, and check them against modal behaviour."
sources:
  - "https://www.mathworks.com/help/slcontrol/ug/linearize.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Extracting stability derivatives

**Goal:** get `X_u, Z_w, M_alpha, M_q, ...` from a model that has no closed-form derivative tables.

## Method A: linearisation
1. Trim at the flight condition (see operating-point-trim).
2. Linearise with `linearize(model, io, op)` with the states, inputs and outputs in a known order (record the state order from the model).
3. For body-axis states `[u w q theta]`, the entries of `A` are the dimensional derivatives divided by mass or inertia: for example `A(1,1) = X_u/m`, `A(3,3) = M_q/Iy`, with the `w-dot` terms folded in by the state-space normalisation. Check your reference for whether `Z_wdot` and `M_wdot` have been moved into `A`.
4. Convert to non-dimensional form only when needed: multiply by the reference length, speed and dynamic pressure factors in your textbook's convention.

## Method B: central differences
1. From the trim state, perturb one state at a time (for example +/- 1 percent speed, +/- 0.5 degree angle of attack, small rates).
2. Evaluate the forces and moments from the model at each perturbed state, with controls frozen.
3. `derivative = (F(+d) - F(-d)) / (2d)`. Check that halving `d` changes the answer by little.

## Checks
- Eigenvalues of the extracted `A` match the model's short-period and phugoid frequency and damping.
- Signs: `M_alpha < 0` for a statically stable aircraft; `M_q < 0`; `Z_w < 0`.

## Gotchas
- Units: body rates in rad/s, angles in rad, otherwise derivatives are off by 57.3.
- Thrust and propulsive terms depend on the engine model; decide whether they are inside the derivative.
- Step too small gives noise; too large gives nonlinearity.

## Verify
- [ ] Rebuilt `A` reproduces a 1 degree elevator step within a few percent of the nonlinear response.

## Checked
2026-11-01. Confirmed on the MathWorks linearize page: `linearize(model, io, op)` form. Removed: the textbook source and the `getstatename` and Model Linearizer references (not on the page read). The A-matrix relations and finite-difference formula are derivations, not documentation claims.
Method: documentation only; no commands were run.
