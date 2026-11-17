---
id: engineering-technology.chemical-engineering.process-control.soft-sensor-development
name: soft-sensor-development
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-performance-monitoring, soft-sensor-development, soft-sensor, inferential-measurement, pls-regression]
level: practitioner
status: draft
description: "Develop an inferential soft sensor: data selection, model fitting, validation, bias updating and monitoring in operation."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Soft sensor development

**Goal:** Develop an inferential soft sensor: data selection, model fitting, validation, bias updating and monitoring in operation.

## Steps
1. Define the target quality variable and its lab or analyzer data with the time stamps and the delay.
2. Select the inputs by process knowledge (temperatures, pressures, flows) and clean the data (remove startups, outliers, align the time).
3. Fit the model: linear regression or PLS for correlated inputs, or a first-principles model with a few fitted parameters; keep it simple.
4. Validate on a separate data set covering the operating range; check the physical behaviour.
5. Deploy with a bias update from the lab results, a range check and monitoring of the model error over time.

## Gotchas
- A model outside the training range is unreliable; add limits.
- Control actions based on the model need an overriding safety check.

## Verify
- [ ] Validation error is within the requirement.
- [ ] Drift monitoring is in place.
