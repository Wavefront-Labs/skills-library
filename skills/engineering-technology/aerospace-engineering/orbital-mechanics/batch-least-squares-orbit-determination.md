---
id: engineering-technology.aerospace-engineering.orbital-mechanics.batch-least-squares-orbit-determination
name: batch-least-squares-orbit-determination
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [batch-least-squares, orbit-determination, state-transition-matrix, weighted-least-squares, estimation, measurement-residuals]
level: practitioner
status: draft
description: "Estimate an orbit with weighted batch least squares: state transition matrix, measurement partials, iteration, residual checks and covariance."
sources:
  - "Tapley, Schutz and Born, Statistical Orbit Determination"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Batch least squares orbit determination

**Goal:** the epoch state that best fits a batch of tracking measurements.

## Algorithm
1. Reference state `X0*` at epoch; propagate it with the state transition matrix `Phi(t, t0)` (integrate variational equations with the state).
2. For each measurement `Y_i` (range, range rate, azimuth and elevation, GNSS position), compute the residual `y_i = Y_i - G(X*(t_i))` and the partial `H_i = (dG/dX) Phi(t_i, t0)`.
3. Normal equations: `(H^T W H) dx0 = H^T W y`, with weights `W = diag(1/sigma^2)`; with an a priori estimate add `P0^-1`.
4. Update `X0 = X0* + dx0` and iterate until the correction or the weighted RMS stops changing.
5. Covariance `P = (H^T W H)^-1`.

## Checks
- Weighted RMS of residuals near 1 if measurement sigmas are right; much larger means model errors or bad data.
- Residual plots by station and type for bias and trends.
- Observability: condition number of `H^T W H`; a short arc or poor geometry makes it ill-conditioned.
- Compare solutions from two disjoint arcs.

## Practice
- Edit outliers using residual thresholds (for example 3 to 5 sigma) with justification.
- Solve for additional parameters (`Cd`, `Cr`, measurement biases) only when observable.
- Use QR or SVD in place of normal equations for ill-conditioned problems.

## Gotchas
- Time tags and light-time corrections for range data.
- Units and angle wrapping in residuals.
- Estimating drag over a short arc absorbs other errors.

## Verify
- [ ] Simulated measurements with known noise recover the true state within the predicted covariance.
