---
id: engineering-technology.aerospace-engineering.matlab-simulink.lqr-design-matlab
name: lqr-design-matlab
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, control-design-matlab, lqr, lqi, bryson-rule, state-feedback, integral-action]
level: practitioner
status: docs-checked
description: "Design an LQR regulator for an aircraft linear model with lqr, choose Q and R using Bryson's rule, add integral action, and check margins."
sources:
  - "https://www.mathworks.com/help/control/ref/lti.lqr.html"
  - "https://www.mathworks.com/help/control/ref/ss.lqi.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# LQR design in MATLAB

**Goal:** state-feedback gains with an interpretable cost.

## Commands
```matlab
[K, S, P] = lqr(sys, Q, R);    % u = -K x; P = closed-loop poles; optional cross term N
% with integral action on the output tracking error:
[K, S, e] = lqi(sys, Q, R);    % e = closed-loop eigenvalues
```
## Choosing weights
The lqr page suggests Bryson's rule for the initial Q and R: `Q_ii = 1/(max acceptable x_i)^2`, `R_jj = 1/(max acceptable u_j)^2`. Start there and scale Q up to speed the response.

## Procedure
1. Scale states and inputs to similar magnitude.
2. Choose Q and R from Bryson's rule; compute K.
3. Close the loop (`feedback` or build in Simulink) and simulate step responses; check control surface rates and deflections against actuator limits.
4. Check margins in the loop broken at the plant input (see margin skill), with actuator dynamics in the model.
5. Add integral action for tracking (`lqi`) and an observer for unmeasured states where needed.

## Gotchas
- High gain LQR demands actuator bandwidth beyond reality: include actuators in the model.
- Check margins again after adding an estimator.

## Verify
- [ ] Closed-loop eigenvalues are stable and as expected.
- [ ] Peak control deflection and rate in the design manoeuvre are within limits.

## Checked
2026-11-01. Confirmed on the MathWorks lqr and lqi pages: lqr syntax and outputs (third output is the closed-loop poles P), u = -Kx, optional N, Bryson's rule for Q and R; lqi outputs (K, S, e) and integrators acting on the reference-minus-output error. Removed: textbook sources, the guaranteed-margin claim and the kalman/lqg names (not on the pages read).
Method: documentation only; no commands were run.
