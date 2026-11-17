---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.driveline-lash-and-compliance-model
name: driveline-lash-and-compliance-model
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [driveline-compliance-model, driveline, backlash, shuffle, halfshaft, torsional-spring, simulink]
level: practitioner
status: gated
description: "Model driveline torsional compliance and gear lash in Simulink to reproduce shuffle, with spring-damper values and the step-size consequences."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
  - "Simulink Backlash block (https://www.mathworks.com/help/simulink/slref/backlash.html)"
  - "Simscape Driveline: Gear with Backlash (https://www.mathworks.com/help/sdl/ug/gear-with-backlash.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Driveline lash and compliance model

**Goal:** a two- or three-inertia model that shows tip-in/tip-out shuffle for controller design.

1. Lump engine/motor+flywheel `Jm`, equivalent vehicle inertia at wheels `Jv = m*Re^2` (plus wheels), and one torsional spring `k` (halfshafts dominate; reflect through final drive to a common shaft) with damper `c`.
2. Natural frequency estimate: `f = (1/2pi)*sqrt(k*(Jm+Jv)/(Jm*Jv))`; typical shuffle is a few Hz (often 3-10 Hz depending on gear (gated: unconfirmed, source is paywalled or blocked); verify against vehicle data). The formula was checked numerically against the eigenvalues of the two-inertia model.
3. Damper: choose damping ratio 0.05-0.2 for the bare driveline as a starting range (gated: unconfirmed, source is paywalled or blocked); tune from measured response.
4. Lash: dead-zone on the twist angle with half-width `alpha/2` (a fraction of a degree to a few degrees at wheel), implemented with the Simulink Backlash block (deadband width and initial output parameters) or the Simscape Driveline Simple Gear block with backlash enabled (spring-damper or coefficient-of-restitution model).
5. Reflect torque through gear and final-drive ratios consistently; sign errors here are the most common bug.

**Gotchas:** lash plus stiff spring is a stiff system; use a variable-step stiff solver offline and a small fixed step (e.g. well under 1/10 of the shuffle period) if the model must go real time.

## Verify
- [ ] Step torque excites a damped oscillation near the predicted frequency.
- [ ] Zero-lash limit recovers the rigid-body acceleration m*a = T/Re.
