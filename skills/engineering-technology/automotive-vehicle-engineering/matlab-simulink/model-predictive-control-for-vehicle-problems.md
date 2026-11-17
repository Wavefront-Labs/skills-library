---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.model-predictive-control-for-vehicle-problems
name: model-predictive-control-for-vehicle-problems
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [model-predictive-control, mpc, mpc-controller-block, constraints, prediction-horizon, adaptive-cruise]
level: practitioner
status: gated
description: "Set up an MPC for a vehicle task such as adaptive cruise or torque coordination: model, horizons, weights, constraints and the solver-time budget."
sources:
  - "Model Predictive Control Toolbox: mpc (https://www.mathworks.com/help/mpc/ref/mpc.html)"
  - "Rawlings, Mayne and Diehl, Model Predictive Control"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# MPC for vehicle problems

1. State the task: e.g. gap control with acceleration limits, or coordinating motor and engine torque. Write inputs (manipulated), outputs (controlled) and measured disturbances.
2. Linear prediction model in discrete state space at the controller sample time (0.05-0.2 s typical for longitudinal tasks (gated: unconfirmed, source is paywalled or blocked); match the actual rate).
3. `mpcobj = mpc(plant, Ts, P, M)`: prediction horizon P covering the settling time in samples, control horizon M much smaller (the toolbox default is 2, with defaults P = 10 plus delay steps; 2-5 is a common choice) to limit computation.
4. Weights: output weights set tracking priority, `ManipulatedVariablesRate` weights give smoothness. Increase rate weight if inputs chatter.
5. Constraints: hard on input limits and rates, soft (with slack) on outputs such as minimum gap, to keep feasibility.
6. Embed with the MPC Controller block; check worst-case execution time for the target; consider explicit MPC or a simpler PI for tight CPUs.

**Gotchas:** infeasible QPs when limits are hard on outputs; model mismatch with large grade changes (use adaptive or scheduled model).

## Verify
- [ ] Constraint violations absent in closed-loop simulation across disturbance cases.
- [ ] Execution time fits the task budget with margin on target hardware.
