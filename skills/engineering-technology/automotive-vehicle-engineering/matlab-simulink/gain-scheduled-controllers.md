---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.gain-scheduled-controllers
name: gain-scheduled-controllers
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [gain-scheduling, scheduled-controller, lookup-table-controller, bumpless-transfer, simulink]
level: practitioner
status: gated
description: "Design gain-scheduled controllers: tune at several operating points, interpolate gains by a slowly varying variable, and prevent switching transients."
sources:
  - "Simulink Control Design: linearize (https://www.mathworks.com/help/slcontrol/ug/linearize.html)"
  - "pidtune (https://www.mathworks.com/help/control/ref/dynamicsystem.pidtune.html)"
  - "Astrom and Murray, Feedback Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Gain-scheduled controllers

1. Pick a scheduling variable that tracks the dynamics and varies slowly: vehicle speed, engine speed, gear, SOC. Avoid scheduling on the controlled output.
2. Grid operating points (5-10 points is a rule of thumb (gated: unconfirmed, source is paywalled or blocked)); linearise and tune each (`pidtune(sys,'PI',wc)`).
3. Store gains in lookup tables indexed by the scheduling variable; use linear interpolation.
4. Implement in a form that avoids bumps when gains change: keep the integrator state scaled (e.g. integrate `Ki*e` rather than `e`) or use the velocity form.
5. Verify stability between grid points by tuning at midpoints and by simulating slow sweeps of the scheduling variable.
6. Discrete-time: use the target sample time and check bandwidth versus step size.

**Gotchas:** scheduling on a noisy signal; add a rate limiter or filter on the scheduling variable.

## Verify
- [ ] Step response at midpoints meets spec.
- [ ] Sweeping the schedule variable shows no output jump.
