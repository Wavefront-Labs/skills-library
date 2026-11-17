---
id: engineering-technology.chemical-engineering.process-control.level-loop-averaging-control
name: level-loop-averaging-control
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-pid-tuning, level-loop-averaging-control, level-control, averaging-level-control, integrating-process, surge-tank, p-only-control, flow-smoothing, level-tuning, buffer-tank]
level: practitioner
status: verified
description: "Tune tank level controllers as averaging controllers (low gain) to smooth outflow, or tight control for reflux drums, with gain and integral time calculations."
sources:
  - "Skogestad, S. (2003) Simple analytic rules for model reduction and PID controller tuning, Journal of Process Control 13(4):291-309, https://doi.org/10.1016/S0959-1524(02)00062-8"
  - "Seborg, Edgar, Mellichamp and Doyle, Process Dynamics and Control (textbook, method only)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Level loop and averaging control

**Goal:** level control that uses the vessel's surge volume to smooth flow disturbances.

## Integrating process
For a tank, A dh/dt = F_in - F_out, so the level is an integrating process with no steady-state self-regulation. A PI controller on an integrating process needs an integral time not too short (otherwise sustained oscillation).

## Averaging control
Goal: let the level float between low and high limits while the outflow changes as slowly as possible.
1. Choose the allowable level range (high-high to low-low alarms with margin) and the maximum acceptable outflow change.
2. **P-only** (or PI with very large Ti): Kc = DF_out,max/Dh_range (in consistent units); for example if the tank level may swing 40% of span while outflow may vary at most 20% of its range, Kc = 0.5 (output percent per level percent).
3. With PI on the integrating process, the SIMC rules give Kc = 1/(k'(tau_c + theta)) and Ti = 4(tau_c + theta), which is equivalent to Ti = 4/(k' Kc) with k' the integrator gain (Skogestad 2003); the integral action is then slow and does not cause oscillation.
4. Validate with a disturbance of the largest expected inflow step: the level must stay within the limits.

## Tight control
When level is part of a product inventory with downstream sensitivity (reflux drums, boilers), use higher Kc with a shorter Ti, and consider feed-forward from inflow (three-element boiler drum control).

## Practice
- Include the valve and the downstream line as part of the process; verify the valve does not saturate.
- For cascade (level to flow), the flow loop must be much faster than the level loop (see `engineering-technology.chemical-engineering.process-control.cascade-control-design`).
- Beware of a nonlinear tank geometry (horizontal drum, conical bottom): gain varies with level.

## Gotchas
- Aggressive PI on a level loop with a small volume produces a cycle in flow that disturbs the downstream unit.
- Level measurement noise (boiling, foam) needs filtering.

## Verify
- [ ] Simulated or tested step in inflow keeps level within limits and flow change within the allowed rate.
- [ ] No sustained cycling over a long observation window.
