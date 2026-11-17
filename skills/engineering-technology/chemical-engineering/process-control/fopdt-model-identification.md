---
id: engineering-technology.chemical-engineering.process-control.fopdt-model-identification
name: fopdt-model-identification
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-process-dynamics, fopdt-model-identification, fopdt, step-response, model-identification]
level: practitioner
status: verified
description: "Identify a first-order plus dead-time model (gain, time constant, delay) from a step test for controller tuning."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fopdt model identification

**Goal:** Identify a first-order plus dead-time model (gain, time constant, delay) from a step test for controller tuning.

## Steps
1. Apply a step in the controller output in manual mode at a steady state and record the process variable until it settles.
2. Gain K = change in PV / change in output (in consistent engineering units or percent of span).
3. Tangent method: draw the tangent at the steepest slope; the dead time is where it crosses the initial value and the time constant from the intersection with the final value (rough).
4. Two-point method: tau = 1.5 (t63 - t28), theta = t63 - tau, where t28 and t63 are the times at 28.3 and 63.2 percent of the final change (checked numerically on a simulated FOPDT step: K=2, tau=7, theta=3 returns tau=7.003, theta=2.994).
5. Validate by simulating the model against the data and a second test in the opposite direction.

## Gotchas
- Nonlinear processes give different gains at different operating points.
- Noise and drift corrupt the tangent method; prefer a regression fit.

## Verify
- [ ] Model overlays the step data.
- [ ] Gain sign and units are right.
