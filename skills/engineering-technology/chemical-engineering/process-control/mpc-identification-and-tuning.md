---
id: engineering-technology.chemical-engineering.process-control.mpc-identification-and-tuning
name: mpc-identification-and-tuning
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-multivariable-control, mpc-identification-and-tuning, model-predictive-control, mpc, system-identification, prbs, step-test, move-suppression, prediction-horizon, constraint-handling, apc]
level: advanced
status: gated
description: "Plan MPC model identification (step or PRBS tests, step-response or FIR models) and tuning of horizons, move suppression and constraint priorities for a process unit."
sources:
  - "Seborg, Edgar, Mellichamp and Doyle, Process Dynamics and Control (textbook, method only)"
  - "Smith and Corripio, Principles and Practice of Automatic Process Control (textbook)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MPC model identification and tuning

**Goal:** a validated multivariable controller model and tuning that performs well and safely. Implementation in a production plant requires the vendor's engineers and operations, safety review and management of change.

## Preparation
1. **Pre-test**: check instruments, valves (stiction), regulatory loops are tuned and base loops stable; define MVs (manipulated), CVs (controlled), DVs (disturbances) and constraints.
2. Estimate time to steady state (settling time) for each CV; set test duration to several settling times.

## Identification
1. **Step tests** (one MV at a time, 3 to 5 steps, amplitude large enough to exceed noise, such as 3 to 10 times the noise band (gated: unconfirmed, source is paywalled or blocked), within safe limits) or **PRBS / multistep tests** with all MVs moved simultaneously and independent patterns; the latter reduces test time and gives better models for interacting plants.
2. Fit models (finite impulse response, step response, or transfer functions with delay) using the vendor's identification tool; check the gain signs and the magnitudes against engineering expectations (for example a RGA check).
3. Validate on data not used in fitting; check the prediction error and the cross-correlation of residuals; refine problem channels.

## Tuning
- **Prediction horizon** at least the longest model settling time (in sampling steps); **control horizon** short (3 to 10 moves (gated: unconfirmed, source is paywalled or blocked)).
- **Move suppression** (weights on input moves) trades speed against robustness; raise it for model uncertainty or noisy outputs.
- **CV weights and priorities**: rank constraints (safety limits highest, quality next, economics last); soft constraints with penalty weights.
- **Steady-state optimisation** layer (LP or QP): economic objective with limits; verify that the optimiser does not push the unit to unsafe or untested regions.
- **Commissioning**: start with CVs in a narrow range and the MV move limits small; progressively widen.

## Gotchas
- Poor model gain on a key CV causes an aggressive wrong move; test with a simulation.
- MPC performance decays as the plant changes; schedule model maintenance.

## Verify
- [ ] Model validation plots saved and signed off.
- [ ] A commissioning plan with step limits, safeguards and a tested switch-off to base controls.
