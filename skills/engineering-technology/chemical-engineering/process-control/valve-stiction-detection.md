---
id: engineering-technology.chemical-engineering.process-control.valve-stiction-detection
name: valve-stiction-detection
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-performance-monitoring, valve-stiction-detection, valve-stiction, stick-slip, control-valve-diagnosis]
level: practitioner
status: draft
description: "Detect control valve stiction from the PV-OP plot and shape-based tests, and distinguish from other causes of oscillation."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Valve stiction detection

**Goal:** Detect control valve stiction from the PV-OP plot and shape-based tests, and distinguish from other causes of oscillation.

## Steps
1. Plot the PV against the OP in a limit cycle: stiction typically gives a distinctive parallelogram-like loop with jumps in the OP-PV relation.
2. Run a bump test: small OP steps in manual and observe if the valve responds only above a threshold (the deadband or stick band).
3. Use the data-based indices (cross-correlation, the shape-based methods) as screening and confirm in the field.
4. Distinguish from tuning-related oscillation (changes with controller gain), external disturbance (appears in several loops), and backlash.
5. Fix by repairing the valve packing and the positioner calibration; do not mask with the controller tuning.

## Gotchas
- A flow loop with a fast response may show the symptoms differently.
- Valve maintenance may need an outage.

## Verify
- [ ] Bump test confirms the stick band.
- [ ] Oscillation stops after the repair.
