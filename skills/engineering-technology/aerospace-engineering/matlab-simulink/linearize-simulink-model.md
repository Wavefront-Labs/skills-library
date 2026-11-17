---
id: engineering-technology.aerospace-engineering.matlab-simulink.linearize-simulink-model
name: linearize-simulink-model
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, trim-linearization, linearize, linmod, state-space, io-points, simulink-control-design]
level: practitioner
status: docs-checked
description: "Linearise a Simulink flight model at a trim point with linearize or linmod, define inputs and outputs, and check that the result matches expectations."
sources:
  - "https://www.mathworks.com/help/slcontrol/ug/linearize.html"
  - "https://www.mathworks.com/help/simulink/slref/linmod.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Linearizing a Simulink model

**Goal:** `A, B, C, D` matrices about a trim point.

## Steps
1. Define analysis points (inputs and outputs) on signals: `io(1) = linio('model/Elevator', 1, 'input'); io(2) = linio('model/Pitch rate', 1, 'output');`
2. Linearize at the operating point: `sys = linearize('model', io, op);`
3. Or use core Simulink `[A,B,C,D] = linmod('model', x, u)`.
4. Inspect the result: check dimensions and that unneeded actuator or sensor states do not clutter the model.
5. Reduce to longitudinal and lateral sets using state selection if needed.

## Practice
- Linearize at several trim points across the envelope for gain scheduling.
- Use `slLinearizer` for multi-point linearization and many I/O combinations.
- A Saturation block whose input is outside its limits linearizes analytically to zero; the linearize page shows setting its `LinearizeAsGain` parameter to off for such a case.

## Gotchas
- Blocks without analytic linearizations are perturbed numerically; the default perturbation is 1e-5(1+|x|). Full-model numerical perturbation is chosen with the `LinearizationAlgorithm` option (`numericalpert` or `numericalpert2`).
- `linearize` turns block reduction off by default; enable it through `linearizeOptions`.

## Verify
- [ ] Eigenvalues of `A` show the expected short-period and phugoid modes.
- [ ] A step input to the linear and nonlinear models agree for small amplitudes.

## Checked
2026-11-01. Confirmed on the linearize and linmod pages: `linearize(model, io, op)` with linio points and OperatingPoint objects, `[A,B,C,D] = linmod(mdl, x, u)`, saturation and LinearizeAsGain behaviour, default perturbation, LinearizationAlgorithm options, BlockReduction default. Removed: lookup-table and rate-limiter statements, the silently-dropped-offset claim and the StateName inspection (not stated on the pages read).
Method: documentation only; no commands were run.
