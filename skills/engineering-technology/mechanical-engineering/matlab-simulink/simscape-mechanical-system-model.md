---
id: engineering-technology.mechanical-engineering.matlab-simulink.simscape-mechanical-system-model
name: simscape-mechanical-system-model
category: engineering-technology
field: mechanical-engineering
product: matlab-simulink
tags: [matlab, simulink, simscape, simscape-multibody, physical-modelling, lumped-parameter, mass-spring-damper, system-dynamics, solver-configuration, ode15s, ode23t, stiff-solver, simscape-logging, parsim, parameter-sweep, simulationinput, natural-frequency, model-verification, 1d-simulation]
level: practitioner
status: docs-checked
description: "Build and verify a lumped-parameter mechanical system in Simscape: blocks, solver configuration, logging, hand-check of natural frequency and parsim parameter sweeps."
sources:
  - "https://www.mathworks.com/help/simscape/ref/solverconfiguration.html"
  - "https://www.mathworks.com/help/simscape/ref/translationalspring.html"
  - "https://www.mathworks.com/help/simscape/ref/sscexplore.html"
  - "https://www.mathworks.com/help/simulink/slref/parsim.html"
  - "https://www.mathworks.com/help/simulink/slref/simulink.simulationinput.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Simscape mechanical system model — physical networks you can trust

**Goal:** a Simscape model of a mechanical (or electro-/hydro-mechanical) system whose
response matches a hand-derived check, runs on a sensible solver, and can be swept over
parameters in a script.

## 1. Start from a hand model
Write the lumped equations first, e.g. a mass-spring-damper `m x'' + c x' + k x = F(t)`.
Compute the checks you will compare against:

```matlab
m = 2; k = 8e3; c = 20;            % kg, N/m, N*s/m
wn = sqrt(k/m); fn = wn/(2*pi);    % 63.2 rad/s, 10.1 Hz
zeta = c/(2*sqrt(k*m));            % 0.079
xs = 100/k;                        % static deflection for 100 N step
```

## 2. Build the physical network
Mechanical translational elements (spring, damper, mass, sources, sensors, reference)
live under **Simscape > Foundation Library > Mechanical > Translational Elements**; the
Translational Spring has ports R (rod) and C (case), with positive force acting from R
toward C. Rotational equivalents exist for shafts. Drive the network from a Simulink
signal and read results back through the Simscape converter blocks.

- **Each physical network (connected Simscape diagram) needs one `Solver Configuration`
  block.**
- Use variables (`m`, `k`, `c`) in block dialogs, not typed numbers, and set the unit
  explicitly in every parameter; a spring typed as `8` with unit `N/mm` is 8000 N/m, a
  frequent silent error when copying.
- Port polarity sets the sign convention (for the spring, R to C is positive); check it
  once with a known static load.

## 3. Initial conditions
Each block exposes initial targets (set in its Initial Targets section). Set a target
only where you need a specific start; conflicting targets give an initialisation error.
Inspect what was actually achieved after the first run.

## 4. Solver
- Pick the Simulink solver by testing: tighten the tolerance, compare, and keep the
  tighter setting if results move noticeably. Choose a maximum step small enough that
  plots are not under-sampled (a fraction of the shortest period of interest).
- For real-time / HIL, turn on **Use local solver** in Solver Configuration (off by
  default). Options are Backward Euler (default, more stable, damps oscillations),
  Trapezoidal Rule (captures oscillations better, less stable) and Partitioning (splits
  the equations to speed up real-time runs). Re-verify against the variable-step run.

## 5. Logging and post-processing
Enable Simscape simulation-data logging in the model configuration, simulate, then
browse the log variable with the Simscape Results Explorer:

```matlab
sscexplore(simlog)        % simlog = the logged variable in your workspace
```

## 6. Parameter sweeps with parsim

```matlab
mdl = 'msd_model'; kv = linspace(4e3, 16e3, 8);
for i = numel(kv):-1:1
    in(i) = Simulink.SimulationInput(mdl);
    in(i) = in(i).setVariable('k', kv(i));
end
out = parsim(in, 'ShowProgress', 'on');   % serial if no parallel pool can be created
```

`SimulationInput` changes are applied temporarily to the model; prefer `setVariable` to
editing the base workspace in a loop. `parsim` has a `UseFastRestart` option
(default off), not supported for models with To File blocks.

## 7. Gotchas
- Algebraic constraint errors usually mean two masses are rigidly connected with no
  compliance: merge them or add a stiff spring.
- Ideal motion sources impose motion with unlimited power, giving unrealistic forces.
- Hard stops and friction create zero crossings; expect step-size collapse and tune their
  stiffness/damping.
- For 3D linkages move to **Simscape Multibody**; for flexible structures, use reduced-
  order models from FEA rather than many lumped masses.

## Verify
- [ ] Static deflection under a step load equals `F/k` within your tolerance.
- [ ] Free-response frequency and decay match `fn` and `zeta` from the hand model.
- [ ] Results unchanged when the solver tolerance is tightened.
- [ ] Every parameter has an explicit unit; signs checked with a known load.
- [ ] Sweep results vary monotonically/physically with the swept parameter.

## Checked
2026-11-01. Confirmed on the MathWorks pages in `sources`: one Solver Configuration block per
network, Use local solver (default off) and its three solver types, Translational Spring
library path and R/C polarity, `sscexplore(simlog)`, `Simulink.SimulationInput`, parsim serial
fallback and `UseFastRestart`. Removed: other block names, `ode23t`/`ode15s` and tolerance
figures, simlog field paths, converter block names, Variable Viewer, priority levels, textbook
source.
Method: documentation only; no commands were run.
