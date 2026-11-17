---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.spacecraft-modal-survey
name: spacecraft-modal-survey
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [modal-survey, modal-analysis, effective-mass, launch-vehicle-coupling, primary-modes, spacecraft-structures]
level: practitioner
status: draft
description: "Plan and run a spacecraft modal survey: pre-test FE, frequency requirements from the launch vehicle, effective mass, test signature and model correlation."
sources:
  - "NASA GSFC-STD-7000 (GEVS)"
  - "Ewins, Modal Testing: Theory, Practice and Application"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Modal survey

**Goal:** measure the spacecraft's modes to validate the model used in coupled loads analysis.

## Requirements
- The launch vehicle user's guide sets minimum primary frequencies for the payload (axial and lateral), to avoid coupling with launcher modes. Take the numbers from the guide for the chosen vehicle.
- Effective modal mass: modes up to the highest frequency of interest should account for most of the mass (target often 90 percent in each direction).

## Procedure
1. Finite-element modal analysis (for example with a normal-modes solution) with a fixed interface or free-free condition; compute effective masses and mode shapes.
2. Pre-test analysis: pick sensor locations and shaker locations.
3. Test: base-driven sine sweep at low level or random excitation, or shaker modal test; measure transfer functions to extract frequencies, damping and shapes.
4. Repeat low-level sine sweeps before and after higher-level vibration tests as a signature check: a frequency shift beyond the programme's threshold indicates damage or looseness.
5. Correlate the model (see fe-model-test-correlation) and deliver a reduced-order model (Craig-Bampton) for the launcher's coupled loads analysis.

## Gotchas
- Modal mass of the test fixture and its dynamics must be removed or modelled.
- Non-linear joints and deployed-mechanism stowed friction shift frequencies with amplitude.
- Correlate in the same configuration as flight (stowed, fuelled or with simulated propellant mass).

## Verify
- [ ] The correlated model reproduces the test frequencies and mode shapes within the correlation criteria and effective masses are reported.
