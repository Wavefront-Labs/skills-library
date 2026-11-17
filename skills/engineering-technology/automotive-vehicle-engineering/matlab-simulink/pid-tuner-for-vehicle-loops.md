---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.pid-tuner-for-vehicle-loops
name: pid-tuner-for-vehicle-loops
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [pid-tuner, pid, pidtune, loop-shaping, speed-control, cruise-control, simulink, controller-design]
level: practitioner
status: gated
description: "Tune a vehicle speed or torque loop with PID Tuner and pidtune, choose bandwidth and phase margin, and check robustness to plant variation."
sources:
  - "pidtune (https://www.mathworks.com/help/control/ref/dynamicsystem.pidtune.html)"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Tune a vehicle loop with PID Tuner

1. Linearise the plant around the operating point (see model-linearization) or identify a first-order-plus-delay model.
2. `C = pidtune(G, 'PI', wc)` sets crossover wc; start with wc about one-tenth of the actuator/plant lag bandwidth, then raise (heuristic (gated: unconfirmed, source is paywalled or blocked)). Use the PID Tuner app sliders for response time and transient behaviour.
3. Check margins `margin(C*G)`: aim for phase margin 45-60 deg and gain margin above 6 dB as a starting point (textbook rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
4. Retune across the envelope (speed, gear, load); if the plant gain varies by more than about 2x use gain scheduling.
5. Add anti-windup, derivative filter and output saturation matching real actuators before deploying.
6. Validate on the nonlinear model with step and ramp references.

**Gotchas:** tuning on an unconstrained linear model and then hitting torque limits; always test with limits.

## Verify
- [ ] Phase margin and step overshoot meet the stated spec across at least three operating points.
- [ ] Actuator saturation does not cause windup.
