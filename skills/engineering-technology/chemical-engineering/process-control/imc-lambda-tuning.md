---
id: engineering-technology.chemical-engineering.process-control.imc-lambda-tuning
name: imc-lambda-tuning
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-pid-tuning, imc-lambda-tuning, imc-tuning, lambda-tuning, simc, pid-tuning, fopdt, closed-loop-time-constant, robust-tuning, pi-controller, tuning-rules]
level: practitioner
status: gated
description: "Tune PI and PID controllers from an FOPDT model using IMC, lambda and SIMC rules, and select the closed-loop speed from deadtime and robustness needs."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio Principles and Practice of Automatic Process Control, Luyben Process Modeling Simulation and Control, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.aiche.org"
  - "https://doi.org/10.1016/S0959-1524(02)00062-8"
  - "https://skoge.folk.ntnu.no/publications/2003/tuningPID/finalpaper.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IMC and lambda tuning

**Goal:** controller settings from a process model with a single, intuitive speed parameter.

## Model
FOPDT: G(s) = K e^(-theta s)/(tau s + 1), identified from a step test (from a step test and a reaction-curve fit).

## Rules (PI, standard form with Kc and integral time Ti)
- **IMC/lambda** for a self-regulating process: Kc = tau/(K (lambda + theta)), Ti = tau, where lambda is the desired closed-loop time constant. Common choice lambda between theta and 3 theta (gated: unconfirmed, source is paywalled or blocked) (larger lambda gives a slower, more robust loop).
- **SIMC (Skogestad, J. Process Control 13(4):291-309, 2003)**: Kc = tau/(K (tau_c + theta)), Ti = min(tau, 4 (tau_c + theta)); with tau_c = theta for fast and robust tuning. For lag-dominant processes (tau much greater than theta) the min() rule avoids a very slow integral action.
- **PID**: for a FOPDT model derivative adds little; SIMC sets the series-form derivative time to the second (smaller) lag, so add derivative only when the process has one (Skogestad 2003).
- For integrating processes (levels): Kc = 1/(K_i (tau_c + theta)) type rules with Ti = 4 (tau_c + theta), where K_i is the slope of the ramp response; see the level skill.

## Procedure
1. Fit K, tau, theta.
2. Choose lambda (or tau_c) by the loop's role: tight loops lambda about theta; interacting loops, noisy measurements or valves with stiction need slower.
3. Compute Kc and Ti, check the controller form (parallel, series, ISA) of your DCS; convert if needed (units: proportional band = 100/Kc for percent signals).
4. Implement; test with a setpoint step and a load disturbance; adjust lambda up if oscillatory or valve moves too much.

## Gotchas
- Deadtime dominant loops (theta greater than tau) benefit from deadtime compensation (see the Smith predictor skill) rather than higher gain.
- Units of K must match controller input and output units (percent of range).

## Verify
- [ ] Simulated or measured step response shows overshoot below about 10% (for tight tuning) and settling at about 4 lambda or less.
- [ ] Gain and phase margin estimated if available (a gain margin above about 2 is a common target (gated: unconfirmed, source is paywalled or blocked)).
