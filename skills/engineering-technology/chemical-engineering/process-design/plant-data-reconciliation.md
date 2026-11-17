---
id: engineering-technology.chemical-engineering.process-design.plant-data-reconciliation
name: plant-data-reconciliation
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-debottlenecking-and-optimisation, plant-data-reconciliation, data-reconciliation, performance-test, mass-balance]
level: practitioner
status: draft
description: "Reconcile plant measurements to close mass and energy balances, find gross errors and run a performance test."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plant data reconciliation

**Goal:** Reconcile plant measurements to close mass and energy balances, find gross errors and run a performance test.

## Steps
1. Choose a steady period; average the data and check instrument calibration and time alignment.
2. Compare the overall and component balances; large imbalance suggests a meter error or an unmeasured stream.
3. Reconcile by adjusting measurements within their uncertainties (weighted least squares subject to balance constraints), after checking for gross errors.
4. Compute performance indicators (yield, specific energy, efficiency) from the reconciled values with uncertainty.
5. For a formal test, agree the method, instruments and acceptance criteria beforehand.

## Gotchas
- Do not force closure by changing one convenient meter.
- Dynamic or non-steady data give misleading results.

## Verify
- [ ] Reconciled balances close.
- [ ] Adjustments are within instrument uncertainty.
