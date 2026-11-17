---
id: engineering-technology.chemical-engineering.process-control.laplace-transfer-function-modelling
name: laplace-transfer-function-modelling
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-process-dynamics, laplace-transfer-function-modelling, laplace-transform, transfer-function, process-modelling]
level: practitioner
status: verified
description: "Build transfer function models from balances using the Laplace transform: first order, integrating, second order and dead time."
sources:
  - "Seborg, Edgar, Mellichamp and Doyle, Process Dynamics and Control (textbook, method only)"
  - "Pade series check computed with sympy: the difference from e^(-x) starts at -x^3/12"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Laplace transfer function modelling

**Goal:** Build transfer function models from balances using the Laplace transform: first order, integrating, second order and dead time.

## Steps
1. Write the dynamic balance (mass or energy), linearise around the operating point and write in deviation variables.
2. Take the Laplace transform; a first-order process gives G(s) = K/(tau s + 1); an integrating process (level) G(s) = K/s.
3. Dead time contributes e^(-theta s); approximate with a Pade approximation (for example the first-order Pade form (1 - theta s/2)/(1 + theta s/2), which matches e^(-theta s) through the second-order term and has unit magnitude at all frequencies) for analysis.
4. Combine series elements by multiplication and parallel ones by addition; closed-loop transfer function = GcGp / (1 + GcGp).
5. Check the poles for stability and use the final value theorem for steady-state gain.

## Gotchas
- Transfer functions describe linear behaviour near an operating point.
- Units and the direction of gain sign matter.

## Verify
- [ ] Steady-state gain matches the steady-state balance.
- [ ] Poles are in the left half plane for a stable process.
