---
id: engineering-technology.chemical-engineering.process-control.linearisation-and-state-space
name: linearisation-and-state-space
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-process-dynamics, linearisation-and-state-space, linearisation, state-space, eigenvalues]
level: practitioner
status: verified
description: "Linearise nonlinear process models to state space (A B C D) and examine eigenvalues, controllability and observability."
sources:
  - "Seborg, Edgar, Mellichamp and Doyle, Process Dynamics and Control (textbook, method only)"
  - "Checked numerically (sympy/numpy): tank A dh/dt = F - k sqrt(h) linearises to a negative eigenvalue at the steady state; a two-tank cascade has controllability rank 2"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linearisation and state space

**Goal:** Linearise nonlinear process models to state space (A B C D) and examine eigenvalues, controllability and observability.

## Steps
1. Write the nonlinear model dx/dt = f(x,u) and find the steady state f(xs,us) = 0.
2. Linearise: A = df/dx and B = df/du evaluated at the steady state, in deviation variables; the outputs give C and D.
3. Eigenvalues of A give the stability and the time scales (negative real parts for stability).
4. Check controllability and observability from the rank of the corresponding matrices.
5. Use the model for controller design (pole placement, LQR, MPC) and validate against the nonlinear simulation.

## Gotchas
- The linear model is valid only near the point; check the range.
- Scaling the states improves the numerics.

## Verify
- [ ] Steady state residual is zero.
- [ ] Linear and nonlinear step responses agree for small steps.
