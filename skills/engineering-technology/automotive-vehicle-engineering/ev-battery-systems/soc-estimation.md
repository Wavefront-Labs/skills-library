---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.soc-estimation
name: soc-estimation
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [soc-estimation, state-of-charge, coulomb-counting, kalman-filter, ekf, ocv-correction]
level: practitioner
status: gated
description: "Estimate state of charge by coulomb counting with OCV correction and Kalman filtering, with sensor error budget, initialisation and LFP flat-curve handling."
sources:
  - "Plett, Battery Management Systems Vol. 1 and 2"
  - "Linden and Reddy, Handbook of Batteries"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# State of charge estimation

1. Coulomb counting: `SOC(t) = SOC0 - (1/Q)*integral(eta*I dt)`; error accumulates from current-sensor offset/gain and capacity error.
2. OCV correction: after rest (current near zero for minutes), read terminal voltage, convert with the OCV-SOC curve at temperature to reset SOC0.
3. Model-based: extended Kalman filter on an equivalent-circuit model; state vector SOC and RC voltages; measurement is terminal voltage; tune process and measurement noise from test data.
4. Error budget: current sensor accuracy, ADC, temperature, capacity learning; typical production targets are a few percent SOC (gated: unconfirmed, source is paywalled or blocked) (check programme requirement).
5. Initialisation after long sleep: use OCV after relaxation; track relaxation time.
6. LFP: flat OCV between about 20 and 90% SOC (gated: unconfirmed, source is paywalled or blocked) makes voltage-based correction poor and adds hysteresis; rely on coulomb counting and full-charge/low-end correction.
7. Test: dynamic profiles (drive cycle), temperature range, aged cells, with a reference SOC from a cycler.

**Gotchas:** sign convention for current; cell-to-cell SOC differences versus pack SOC definition.

## Verify
- [ ] Maximum SOC error under validation profiles meets the requirement.
- [ ] Recovery from wrong initial SOC demonstrated.
