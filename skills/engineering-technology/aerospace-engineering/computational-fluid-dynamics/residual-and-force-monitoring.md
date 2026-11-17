---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.residual-and-force-monitoring
name: residual-and-force-monitoring
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, convergence, solver-convergence, residuals, force-monitors, drag-counts, convergence-criteria, monitor-points]
level: practitioner
status: draft
description: "Judge convergence by residuals and engineering quantity monitors together, with practical thresholds and the signs of a false convergence."
sources:
  - "Solver user guides (monitoring convergence)"
  - "Blazek, Computational Fluid Dynamics Principles and Applications"
  - "AIAA Drag Prediction Workshop practice"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Residuals and force monitors

**Goal:** know the solution has converged before using it.

## Criteria
1. **Residuals:** typically drop 3-4 orders of magnitude (or to a flat level of 1e-5 or lower for scaled residuals) but the level depends on scaling; do not trust a single threshold.
2. **Force monitors:** lift, drag and moment coefficients flat over the last several hundred iterations; for drag, variation below about 1 drag count (0.0001) is a common requirement for aircraft drag work.
3. **Field monitors:** point values or integrated mass flow imbalance below about 0.1-1% of the inflow.
4. **Conservation:** global mass and energy balance.

## Practice
- Plot all of them on the same iteration axis; define the averaging window in advance.
- Residual plateaus above target often indicate unsteadiness: check for force oscillations.
- Restart the case and compare final results.

## False convergence
- Residuals fall because a first-order scheme or heavy limiter is active.
- Residuals normalised by an initially large value make a poor run look good.
- Forces flat only because they are not on the sensitive quantity (for example separation point).

## Verify
- [ ] Forces, residuals and imbalance meet the pre-set criteria for a stated window.
- [ ] Extra iterations change the quantity of interest by less than the tolerance.
