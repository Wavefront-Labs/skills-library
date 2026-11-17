---
id: engineering-technology.aerospace-engineering.matlab-simulink.ode-event-detection
name: ode-event-detection
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, trajectory-integration, trajectory-analysis, ode-integration, event-detection, odeset, ode45, ground-impact]
level: practitioner
status: docs-checked
description: "Detect ground impact, apogee or stage events in MATLAB ODE integration with odeset Events, terminal flags and direction settings, and restart cleanly."
sources:
  - https://www.mathworks.com/help/matlab/ref/odeset.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ODE event detection

**Goal:** stop or switch integration exactly when a condition is met.

## Pattern
```matlab
function [value, isterminal, direction] = hitGround(t, y)
    value = y(3);         % altitude
    isterminal = 1;       % stop the integration
    direction = -1;       % only when decreasing through zero
end
opts = odeset('Events', @hitGround, 'RelTol', 1e-9, 'AbsTol', 1e-9);
[t, y, te, ye, ie] = ode45(@eom, [0 600], y0, opts);
```
`te, ye, ie` hold the event time, state and event index.

## Practice
1. Use event functions rather than checking the step values (steps can jump past the event).
2. For staging, terminate, change parameters and states, and restart with the final state as the new initial state.
3. Use event direction to avoid false triggers at the start (initial altitude zero).

## Gotchas
- Events at the initial state: shift the event or use direction.
- Discontinuities (thrust cutoff) inside a single call degrade step control: split the integration at the discontinuity.

## Verify
- [ ] A no-drag ballistic case lands at the analytic time `2 v sin(gamma)/g` within tolerance.

## Checked

2026-11-01. Confirmed on the MathWorks odeset page: the `[value,isterminal,direction] = myEventsFcn(t,y)` form,
`isterminal(i) = 1` stops integration, `direction` 0 (all zeros, default) / +1 increasing / -1 decreasing, the
`RelTol` and `AbsTol` option names, and the `[t,y,te,ye,ie]` outputs (event times, solution values, event indices).
Removed: the Simulink zero-crossing / solver-pane remark, which was not on the page.
Method: documentation only; no commands were run.
