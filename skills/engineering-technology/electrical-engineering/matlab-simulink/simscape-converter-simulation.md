---
id: engineering-technology.electrical-engineering.matlab-simulink.simscape-converter-simulation
name: simscape-converter-simulation
category: engineering-technology
field: electrical-engineering
product: matlab-simulink
tags: [matlab, simulink, simscape, simscape-electrical, specialized-power-systems, powergui, power-electronics, converter-simulation, buck-converter, inverter, pwm, averaged-model, switched-model, ode23t, ode15s, local-solver, backward-euler, solver-configuration, simlog, simscape-logging, mosfet, igbt, thermal-model, frestimate, control-design, simscape-solver-configuration]
level: practitioner
status: docs-checked
description: "Build and solve switched and averaged power-converter models in Simscape Electrical: fidelity choice, solver configuration, PWM, logging, losses."
sources:
  - "https://www.mathworks.com/help/simscape/ref/solverconfiguration.html"
  - "https://www.mathworks.com/help/simscape/ref/electricalreference.html"
  - "https://www.mathworks.com/help/simscape/ref/sscexplore.html"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Simscape converter simulation — fast, stable, trustworthy power-electronics models

**Goal:** a converter model that runs in reasonable time, resolves the switching ripple you
care about, and whose results you can trust enough to size parts and tune control.

## 1. Pick the fidelity before you draw anything
| Question | Model |
|---|---|
| Control loop tuning, slow dynamics, grid events (ms-s) | **Averaged** (controlled sources / average-value converter blocks) |
| Ripple, peak currents, losses, dead-time effects | **Switched**, ideal or piecewise-linear switches |
| Switching transients, ringing, EMI | Switched with detailed device models (or move to SPICE) |

Rule: start averaged, prove the control works, then switch for stress and loss.
Switched models of a high-frequency converter over a long grid event take ages and teach little.

## 2. Network rules
- Every isolated Simscape network needs its own **Solver Configuration** block (one per
  connected physical network).
- A model with electrical elements must contain at least one **Electrical Reference**
  block (Simscape > Foundation Library > Electrical > Electrical Elements, or
  Simscape > Electrical > Connectors & References); wire grounded ports to it. A floating
  network gives a "singular" or "unable to solve" style error.
- The older Specialized Power Systems library (`powergui`-driven) is a separate
  modelling approach; do not mix the two in one circuit without the interface blocks
  your release documents.

## 3. Solver settings
- Variable-step desktop runs: choose a stiff-capable solver, cap the maximum step well
  below the switching period, and confirm convergence by halving it (see Verify).
- Fixed-step / HIL: turn on **Use local solver** in Solver Configuration (off by default).
  Options are Backward Euler (default), Trapezoidal Rule and Partitioning (splits the
  equations to speed real-time runs; read the diagnostics it emits). Use a sample time
  that is an integer sub-multiple of the PWM period.

## 4. Building the switched stage
- Drive gates from a PWM generator or a compare-to-carrier subsystem; insert dead
  time explicitly or the half-bridge shorts.
- Ideal switches with zero off-state conductance across an inductor can make the network
  unsolvable when both are off; give switches a small off conductance or rely on a body
  diode in the device block.
- Set initial conditions (inductor current, capacitor voltage) near steady state so
  start-up does not dominate runtime.
- Losses: use device blocks with data from the datasheet and a thermal network for
  junction temperature; check your release's block pages for the parameterisation.

## 5. Post-processing
Browse logged variables with the Simscape Results Explorer: `sscexplore(simlog)` (the
log variable must be in your workspace). Take ripple from the last whole switching
periods, not the start-up transient.

## 6. Gotchas
- Results that change when you halve the maximum step are not converged; do that check once.
- Algebraic loops between a controller and the plant: add a unit delay that
  represents the real ADC/PWM update delay (it exists in hardware anyway).
- Block names, menu locations and parameter names change across releases; confirm
  against your release's documentation.

## Verify
- [ ] Averaged and switched models agree on average output voltage/current.
- [ ] Halving the max/fixed step does not change ripple and peaks.
- [ ] Steady-state ripple matches the hand calc (e.g. dI = (Vin-Vo)*D/(L*fsw) for a buck).
- [ ] Every Simscape network has a Solver Configuration and an Electrical Reference.
- [ ] Dead time is present and no shoot-through current appears in the switch logs.

## Checked
2026-11-01. Confirmed on the MathWorks pages in `sources`: one Solver Configuration per
network, Use local solver (default off) with Backward Euler / Trapezoidal Rule /
Partitioning, Electrical Reference requirement and library paths, `sscexplore(simlog)`.
Removed: step-size ratios, dead-time and sample-time figures, `ode23t`/`ode15s`, tolerance and
percentage thresholds, `frestimate`, `set_param` logging parameters, MOSFET and thermal details
(pages not readable), textbook sources.
Method: documentation only; no commands were run.
