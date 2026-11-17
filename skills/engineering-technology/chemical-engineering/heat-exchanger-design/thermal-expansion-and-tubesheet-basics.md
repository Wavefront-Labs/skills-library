---
id: engineering-technology.chemical-engineering.heat-exchanger-design.thermal-expansion-and-tubesheet-basics
name: thermal-expansion-and-tubesheet-basics
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-mechanical-and-vibration, thermal-expansion-and-tubesheet-basics, thermal-expansion, tubesheet, expansion-joint, floating-head]
level: practitioner
status: draft
description: "Understand differential thermal expansion in fixed-tubesheet exchangers and when an expansion joint or floating head is needed."
sources:
  - "Kern Process Heat Transfer, Heat Exchanger Design Handbook, TEMA Standards, Kemp Pinch Analysis and Process Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thermal expansion and tubesheet basics

**Goal:** Understand differential thermal expansion in fixed-tubesheet exchangers and when an expansion joint or floating head is needed.

## Steps
1. Compute the metal temperatures of the tubes and shell at operating, startup and upset cases; differential expansion = alpha_tube (T_tube) L - alpha_shell (T_shell) L, approximately.
2. In a fixed tubesheet exchanger, the difference loads the tubes (tension or compression) and the tubesheet joints; check against the allowable stress by the pressure vessel code procedure.
3. If the stress is high, add a shell expansion joint, or choose U-tube or floating head designs (TEMA types).
4. Specify the tubesheet thickness and the tube-to-tubesheet joint (expanded, welded) per the code and the service.
5. Mechanical design is done by the vessel designer to the applicable code (for example ASME Section VIII and TEMA); the process engineer provides the temperature cases.

## Gotchas
- Do not omit upset cases such as loss of one fluid.
- Confirm the current code edition in force for your jurisdiction.

## Verify
- [ ] Metal temperature cases are listed with their durations.
- [ ] Stress check is by a qualified mechanical engineer.
