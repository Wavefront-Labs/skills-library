---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.linearise-model-and-read-bode
name: linearise-model-and-read-bode
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [model-linearization, linearize, bode, margin, operating-point, model-linearizer, simulink]
level: practitioner
status: gated
description: "Linearise a Simulink vehicle model at an operating point, read Bode and step responses, and avoid frequent pitfalls with trim and discontinuities."
sources:
  - "Simulink Control Design: linearize, findop, operspec (https://www.mathworks.com/help/slcontrol/ug/linearize.html)"
  - "isstable (https://www.mathworks.com/help/control/ref/dynamicsystem.isstable.html)"
  - "Astrom and Murray, Feedback Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Linearise a model and read Bode plots

1. Find a steady operating point: `findop`/`operspec` or simulate to steady state and snapshot; check derivatives are near zero.
2. Mark analysis points on the signals (input perturbation, output measurement) rather than breaking the model.
3. `sys = linearize(mdl, io, op)`; check `isstable`, order, and that expected states are present.
4. `bode(sys)`, `margin(sys)`, `step(sys)`. Compare the linear step to a small-amplitude nonlinear simulation: they must agree.
5. Treat discontinuities (saturations, dead zones, lookups with steep slopes, backlash) with care: they linearise to zero or huge gain; replace with smooth equivalents or move the operating point off them.
6. Repeat across the envelope and store as an LTI array for scheduling.

**Gotchas:** linearising at a mode switch; very small blocks of rate limiters produce zero gain (practical observation (gated: unconfirmed, source is paywalled or blocked)).

## Verify
- [ ] Linear vs nonlinear small-signal agreement within a few percent.
- [ ] Poles and gain at the operating point are physically plausible.
