---
id: engineering-technology.chemical-engineering.process-control.step-test-design
name: step-test-design
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-process-dynamics, step-test-design, step-test, plant-test, excitation]
level: practitioner
status: draft
description: "Design a step test: step size, duration, disturbance isolation, safety limits and repeat tests for a reliable process model."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Step test design

**Goal:** Design a step test: step size, duration, disturbance isolation, safety limits and repeat tests for a reliable process model.

## Steps
1. Agree the limits with operations; make sure the steps stay inside safe and quality limits.
2. Choose the step big enough to rise above noise (several times the noise amplitude) and small enough to remain in the linear range; a few percent of the output span is a common starting point.
3. Allow the test duration to cover at least the full response, preferably four to five time constants plus dead time.
4. Hold other loops in manual or constant, and record the disturbances known to occur.
5. Repeat in both directions and at different loads, and keep the data with the sampling time well below the dead time.

## Gotchas
- Disturbances during the test ruin the analysis.
- Tell the operators in advance of the test and the abort criteria.

## Verify
- [ ] Tests are repeatable.
- [ ] Data are time-stamped and saved with the tag list.
