---
id: engineering-technology.chemical-engineering.process-control.anti-windup-and-bumpless-transfer
name: anti-windup-and-bumpless-transfer
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-pid-tuning, anti-windup-and-bumpless-transfer, anti-windup, integral-windup, bumpless-transfer, back-calculation, tracking, manual-auto, saturation, velocity-form, external-reset-feedback]
level: practitioner
status: gated
description: "Implement anti-windup (back-calculation, clamping, tracking) and bumpless transfer between manual and auto, cascade and override modes in PID loops."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio Principles and Practice of Automatic Process Control, Luyben Process Modeling Simulation and Control, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anti-windup and bumpless transfer

**Goal:** avoid integrator windup when the output saturates and avoid output jumps on mode changes.

## Windup
When the valve (or an inner loop setpoint) is saturated, the integral term keeps growing, so after the error changes sign the output stays saturated until the integral unwinds, causing large overshoot and delay.

## Anti-windup methods
1. **Conditional integration (clamping)**: stop integrating when the output is at its limit and the error pushes further into saturation.
2. **Back-calculation (tracking)**: feed the difference between the actual (limited) output and the controller output back to the integrator with a tracking time constant Tt (about the integral time Ti, often between sqrt(Ti Td) and Ti (gated: unconfirmed, source is paywalled or blocked)).
3. **External reset feedback**: use the actual downstream value (valve position or inner-loop measurement) as the integrator feedback; native in many DCS PID blocks; essential for cascade, split-range and override control.
4. **Velocity form** PID: the controller outputs increments, so limits inherently stop windup.

## Bumpless transfer
1. **Manual to auto**: initialise the integrator (or the output bias) so the controller output equals the current manual output; set the setpoint to the measurement (setpoint tracking) or ramp it.
2. **Cascade**: the primary controller tracks the secondary setpoint when the secondary is in auto/local mode.
3. **Override/selector**: the non-selected controller tracks the selected output (external reset).
4. **Gain or setpoint changes**: use setpoint weighting (set the proportional and derivative actions on the measurement) so a setpoint step does not kick the output.

## Practice
- Set output limits to realistic valve limits, not 0 to 100 if the process needs minimum flow.
- Use a derivative filter (N about 5 to 20 (gated: unconfirmed, source is paywalled or blocked)) and derivative on measurement.

## Gotchas
- Different DCS vendors implement tracking differently; read the block documentation.
- Anti-windup alone does not fix a loop that saturates permanently (a design or tuning issue).

## Verify
- [ ] Test: drive the loop into saturation with a large setpoint step and confirm overshoot after recovery is small.
- [ ] Mode-change test shows no output bump.
