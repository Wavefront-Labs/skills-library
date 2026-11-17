---
id: engineering-technology.aerospace-engineering.matlab-simulink.simulation-validation-against-flight-data
name: simulation-validation-against-flight-data
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [simulation-validation, flight-test-comparison, theil-inequality, time-history-matching, model-validation]
level: practitioner
status: draft
description: "Validate a flight simulation against recorded manoeuvre data with matched inputs, quantitative error metrics, and clear acceptance criteria."
sources:
  - "Jategaonkar, Flight Vehicle System Identification"
  - "Stevens and Lewis, Aircraft Control and Simulation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Validating a simulation

**Goal:** show the model reproduces the real aircraft or vehicle well enough for its intended use.

## Procedure
1. Define the intended use and the quantities that matter (short-period response, climb rate, landing loads) before choosing criteria.
2. Select data: frequency-rich manoeuvres (doublets, 3-2-1-1, sweeps) at stated conditions, not just steady points.
3. Drive the model with the recorded control-surface and thrust inputs, from the same initial state, with the same atmosphere and mass properties.
4. Align time (measure transport delay), remove sensor bias, and match units and axes.
5. Compute metrics per output: RMS error, maximum error, and a Theil-type inequality coefficient `TIC = sqrt(sum((y-yhat)^2)) / (sqrt(sum(y^2)) + sqrt(sum(yhat^2)))`. Values near 0 mean close fit; a threshold around 0.3 is often quoted as acceptable in identification literature, but set your own criteria.
6. Inspect residuals for structure; a clean model leaves noise-like residuals.
7. Record limits: where the model has been validated and where it is extrapolating.

## Gotchas
- Open-loop playback of inputs diverges for unstable aircraft; use short windows or the closed-loop commands.
- A good fit on one manoeuvre does not validate other conditions.
- Wind and turbulence during the test must be estimated or the fit absorbs them into derivatives.

## Verify
- [ ] A held-back manoeuvre not used in tuning meets the same criteria.
