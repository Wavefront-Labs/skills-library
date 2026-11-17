---
id: social-sciences.economics.macroeconomic-modelling.solving-and-simulating-dsge-models-with-dynare
name: solving-and-simulating-dsge-models-with-dynare
category: social-sciences
field: economics
product: macroeconomic-modelling
tags: [macroeconomic-modelling, macroeconomics, dsge, dynare, matlab, octave, steady-state, perturbation, impulse-response-functions, calibration, bayesian-estimation, occasionally-binding-constraints, perfect-foresight]
level: advanced
status: docs-checked
description: "Write, solve and simulate a dynamic macro model in Dynare: equation list, steady state, residual checks, simulation, estimation and perfect-foresight workflow."
sources:
  - https://www.dynare.org/manual/
  - https://www.dynare.org/manual/the-model-file.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic macro models in Dynare, from equations to impulse responses

**Goal:** a model whose equilibrium conditions are right, whose steady state is verified,
and whose dynamics you can explain shock by shock.

## 1. Before code: the equation list
Derive every agent's optimality conditions and the market-clearing and resource
constraints. The number of equations must equal the number of endogenous variables.
Write the list on paper with each variable's timing (predetermined state versus jump
variable) before opening Dynare.

## 2. Steady state
- Solve analytically where possible, then check by plugging values back into every
  equation: residuals must be about zero.
- The Dynare `resid` command displays the static equation residuals (it has a `non_zero`
  option). Initial guesses go in an `initval` block (manual section 4.7).
- The manual has a section on providing the steady state explicitly (manual section 4.10).

## 3. Running a model
A `.mod` file is run in MATLAB or GNU Octave (the manual has installation and
configuration instructions for both). Stochastic runs use `stoch_simul`, whose
examples in the manual use `order=1`; shocks are declared in a shocks block (manual
section 4.8). Check the current manual for each option you use. Timing is the most
common bug source: be explicit about which period each stock variable refers to.

## 4. Determinacy
Confirm that the model has a unique stable solution; the manual's section on
stochastic solution and simulation (4.13) is the place to look. Errors here
usually mean a timing mistake, not deep economics.

## 5. Calibration versus estimation
- Calibrate to long-run ratios and micro evidence, and document each source.
- Bayesian estimation uses the manual's sections on observables and trends (4.16.1),
  estimated parameters and priors (4.16.2), and the `estimation` command with its
  MCMC options (4.16.3). Data must be transformed to match model variables.
  Dynare also has a section on identification analysis (4.23.3); report convergence and
  identification diagnostics.

## 6. Reading results
- Trace each impulse response through the equations; explain it in words.
- Compare simulated moments with data filtered the same way.

## 7. Beyond first order
- Occasionally binding constraints: Dynare has an OccBin section (4.15).
- Large shocks and nonlinear transitions: deterministic simulation with
  `perfect_foresight_setup` and `perfect_foresight_solver` (manual section 4.12).

## Gotchas
- Mixing levels and logs across equations; be consistent.
- Setting a shock's standard deviation in two places; know which one wins.
- Label axes: percentage deviations versus percentage-point deviations for rates.

## Verify
- [ ] Equation count equals endogenous variable count; timing annotated.
- [ ] Steady-state residuals all about zero.
- [ ] Solution determinacy checked per the manual.
- [ ] Every calibrated parameter has a source.
- [ ] Estimation: convergence and identification diagnostics reported.

## Checked
2026-11-01. Confirmed in the Dynare manual contents and model-file chapter: `resid` and
its `non_zero` option, `initval`, `stoch_simul` with `order=1` in examples,
`perfect_foresight_setup` and `perfect_foresight_solver`, the headings for shocks,
observables, estimated parameters, the estimation command and MCMC options,
identification analysis, OccBin, steady state, and MATLAB and GNU Octave support.
Removed: NK equations, RBC steady-state formulas, `check` and Blanchard-Kahn details,
`steady_state_model` syntax, `irf=`, `mh_replic`, `mh_nblocks` and `pruning` option
names, the `stderr` form, HP filter figures and the Hamilton reference, the
Galí and Handbook source citations (textbook claims, not checked here).
Method: documentation only; no commands were run.
