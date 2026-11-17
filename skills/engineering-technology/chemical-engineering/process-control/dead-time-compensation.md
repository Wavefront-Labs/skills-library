---
id: engineering-technology.chemical-engineering.process-control.dead-time-compensation
name: dead-time-compensation
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-advanced-regulatory-control, dead-time-compensation, smith-predictor, deadtime-dominant, model-based-control, imc, dahlin, time-delay, long-dead-time]
level: advanced
status: gated
description: "Apply deadtime compensation (Smith predictor, IMC-based) to loops with long deadtime relative to the time constant, understand model mismatch limits and alternatives."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio Principles and Practice of Automatic Process Control, Luyben Process Modeling Simulation and Control, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead-time compensation and Smith predictor

**Goal:** better control of processes whose delay theta is as large as or larger than the time constant tau.

## When PID is enough
For theta/tau below about 0.3 to 0.5 (gated: unconfirmed, source is paywalled or blocked), a well-tuned PID works. For theta/tau around 1 or more, PI with conservative tuning is slow, and compensation can reduce the settling time significantly, if the model is good.

## Smith predictor structure
Controller C acts on the error computed with a model of the process without delay, G_m(s) (the "fast" model), and corrects with the difference between the delayed model and the measurement:
u = C [ r - y - (G_m(s) - G_m(s) e^(-theta_m s)) u ]
In the ideal case (perfect model) the characteristic equation 1 + C G_m = 0 has no delay (algebra checked symbolically: y/r = C G_m e^(-theta s)/(1 + C G_m)), so C can be tuned for the delay-free process (for example with IMC rules with theta = 0); disturbance response still contains delay.

## Practical points
1. Obtain a good FOPDT model (K, tau, theta) by a step test.
2. Tune the controller for the delay-free model with a moderate speed; start slow.
3. The performance is sensitive to mismatch in theta; a delay error of the order of 20% can destabilise a loop tuned aggressively (gated: unconfirmed, source is paywalled or blocked). Test robustness by simulating plus or minus 25% errors in the model gain and delay.
4. In a DCS use a built-in block (deadtime compensator) or build with a delay block and filters; for integrating processes use the modified Smith predictor.
5. Alternatives: MPC (which handles delay in its model), lower-gain PI with a setpoint filter, or a faster measurement (moving analyser closer, an inferential estimate) to cut deadtime at the source.

## Gotchas
- Time-varying delay (transport delay depends on flow) requires scheduling theta with flow.
- A compensator hides a bad analyser sample time; reduce sample delay first.

## Verify
- [ ] Simulation with plus or minus 25% mismatch stays stable.
- [ ] Setpoint response faster than the tuned PI baseline for the same disturbance.
