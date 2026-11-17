---
id: engineering-technology.chemical-engineering.heat-exchanger-design.tube-vibration-assessment
name: tube-vibration-assessment
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-mechanical-and-vibration, tube-vibration-assessment, tube-vibration, flow-induced-vibration, fluidelastic-instability]
level: practitioner
status: draft
description: "Screen shell-and-tube bundles for flow-induced vibration: fluidelastic instability, vortex shedding and acoustic resonance."
sources:
  - "Kern Process Heat Transfer, Heat Exchanger Design Handbook, TEMA Standards, Kemp Pinch Analysis and Process Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tube vibration assessment

**Goal:** Screen shell-and-tube bundles for flow-induced vibration: fluidelastic instability, vortex shedding and acoustic resonance.

## Steps
1. Find the natural frequency of the tube spans between baffles (longest span is critical, usually the inlet and outlet or the unsupported U-bend region).
2. Estimate the crossflow velocity in the windows and at the inlet; compare with the critical velocity for fluidelastic instability, with a safety factor (TEMA and the Heat Exchanger Design Handbook give methods).
3. Check vortex shedding frequency versus the tube natural frequency, and for gases the acoustic standing wave frequency.
4. Fix problems by reducing span (more baffles), changing to a NTIW or double-segmental baffle design, or increasing the tube pitch.
5. Use the vendor or design software tools for the final check.

## Gotchas
- Screening methods are conservative or non-conservative depending on the case; follow the TEMA edition and company practice.
- Gas service and high velocities are the highest risk.

## Verify
- [ ] Critical velocity exceeds the actual velocity with margin.
- [ ] Frequencies are separated.
