---
id: engineering-technology.chemical-engineering.aspen.hysys-dynamic-mode-setup
name: hysys-dynamic-mode-setup
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-sensitivity-and-optimisation, hysys-dynamic-mode-setup, hysys-dynamics, dynamic-mode, pressure-flow-solver]
level: practitioner
status: gated
description: "Prepare an Aspen HYSYS steady-state model for dynamic mode: size equipment, set pressure-flow specs and add controllers before running the integrator."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hysys dynamic mode setup

**Goal:** Prepare an Aspen HYSYS steady-state model for dynamic mode: size equipment, set pressure-flow specs and add controllers before running the integrator.

## Steps
1. Finish the steady-state model, then size every vessel, heat exchanger and column (volumes, heights, nozzles, tray dimensions) because dynamics depends on holdup.
2. Replace fixed-flow boundary specs with pressure-flow behaviour: add valves with realistic pressure drops and use the Dynamics Assistant to check completeness (gated: unconfirmed, source is paywalled or blocked).
3. Add controllers with correct action and ranges and rough initial tuning; put key variables on strip charts.
4. Switch to dynamic mode, run the integrator with a small step, and confirm the model holds steady state with no disturbance.
5. Then apply a step disturbance and check the response is physically sensible.

## Gotchas
- Missing equipment volumes is the commonest cause of a failing integrator.
- Menu names vary by HYSYS version.

## Verify
- [ ] Model holds steady with no disturbance.
- [ ] Controllers respond in the correct direction.
