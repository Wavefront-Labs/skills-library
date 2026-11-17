---
id: engineering-technology.aerospace-engineering.matlab-simulink.pidtune-loop-tuning
name: pidtune-loop-tuning
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [pidtune, pid-tuning, control-system-toolbox, loop-shaping, autopilot-tuning]
level: practitioner
status: docs-checked
description: "Tune PID and PI loops for flight-control plants with pidtune: controller type, target crossover frequency, tuning options, and checking the result against your margin criteria."
sources:
  - https://www.mathworks.com/help/control/ref/dynamicsystem.pidtune.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tuning PID loops with pidtune

**Goal:** a PID, PI or PID with filter that meets bandwidth and margin targets on a linear plant.

## Commands
```matlab
C = pidtune(G, 'PID');             % pidtune chooses the crossover frequency
C = pidtune(G, 'PIDF', wc);        % PID with derivative filter, target crossover wc
opts = pidtuneOptions(<options>);  % tuning options, see the pidtuneOptions page
C = pidtune(G, 'PI', wc, opts);
[C, info] = pidtune(G, 'PID');     % info has Stable, CrossoverFrequency, PhaseMargin
```
The `type` argument selects the structure: 1-DOF `'P'`, `'I'`, `'PI'`, `'PD'`, `'PDF'`, `'PID'`, `'PIDF'`, or 2-DOF
variants such as `'PID2'`. `'PIDF'` adds a first-order filter on the derivative term. `wc` is the target first 0 dB
gain crossover frequency in radians per `TimeUnit` of the plant. Increasing `wc` speeds up the response; decreasing
it improves stability. If you omit `wc`, `pidtune` chooses one.

## Procedure for an attitude or altitude loop
1. Use the linearised plant for the inner loop (for example elevator to pitch rate) and close inner loops first.
2. Choose `wc` below actuator bandwidth and well below structural-mode frequencies.
3. Prefer `PIDF` or `PI` on rate-limited or noisy channels.
4. Read `info.PhaseMargin`, then check gain and phase margins and step plots for overshoot and settling time.
5. Re-check at the edges of the flight envelope (gain scheduling) before accepting.

## Gotchas
- `pidtune` designs for the linear plant given; saturation and rate limits need nonlinear simulation afterwards.
- Passing a `type` returns a parallel-form controller (Kp, Ki, Kd); standard form (Kp, Ti, Td) is returned only
  when you pass a standard-form object as the starting controller `C0`. Do not mix gains between the two forms.
- Units of `wc` are radians per time unit of the plant (rad/s for a plant in seconds), not Hz.

## Verify
- [ ] Margins meet your programme's criteria at all scheduled conditions.

## Checked

2026-11-01. Confirmed on the MathWorks pidtune reference page: syntax forms, the list of types, `'PIDF'` derivative
filter, `wc` meaning and units, `info` fields, parallel versus standard form. Removed because the page does not
state them: the 60 degree default phase margin, the `'PhaseMargin'` option name, `pidTuner`, `margin` / `allmargin`,
the "factor of several" rule of thumb and the 45 degree / 6 dB thresholds.
Method: documentation only; no commands were run.
