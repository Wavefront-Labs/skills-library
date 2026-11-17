---
id: engineering-technology.chemical-engineering.process-control.oscillation-diagnosis
name: oscillation-diagnosis
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-performance-monitoring, oscillation-diagnosis, oscillation-diagnosis, limit-cycle, plantwide-oscillation]
level: practitioner
status: draft
description: "Diagnose plant oscillations: find the period, check which loops share it, and decide whether the cause is tuning, valves or disturbance."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oscillation diagnosis

**Goal:** Diagnose plant oscillations: find the period, check which loops share it, and decide whether the cause is tuning, valves or disturbance.

## Steps
1. Compute the oscillation period from the PV spectrum (a clear peak in the FFT) and the amplitude.
2. Find all tags oscillating at the same period (plant-wide); the source is often the one with the largest amplitude or the nonlinear (non-sinusoidal) shape.
3. Test hypotheses: put the suspect loop in manual; if the oscillation stops, the loop is the source; if it continues, the cause is external.
4. Check for valve stiction, tuning too aggressive, interaction between loops and recycle loops with the integrating action.
5. Apply the fix, and confirm by the spectrum.

## Gotchas
- A slow oscillation may be a daily disturbance such as ambient.
- Take the data at an adequate sampling rate.

## Verify
- [ ] Source loop is identified by the manual test.
- [ ] Peak disappears after the fix.
