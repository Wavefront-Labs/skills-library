---
id: engineering-technology.chemical-engineering.process-design.refrigeration-system-selection
name: refrigeration-system-selection
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-utilities-and-offsites, refrigeration-system-selection, refrigeration, refrigerant-selection, cop]
level: practitioner
status: draft
description: "Select a refrigeration system and refrigerant for process cooling below cooling-water temperature, with COP and staging checks."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Refrigeration system selection

**Goal:** Select a refrigeration system and refrigerant for process cooling below cooling-water temperature, with COP and staging checks.

## Steps
1. List cooling loads by temperature level and pick the lowest necessary levels; do not refrigerate what cooling water can do.
2. Choose the refrigerant for the evaporating temperature and pressure range (for example propane, propylene, ammonia or a halocarbon); check safety, toxicity, flammability and the regulations that apply to refrigerant in your jurisdiction.
3. Choose the cycle: single stage, economised or cascade, depending on the compression ratio and the temperature lift.
4. Estimate power from the refrigeration load and the Carnot-based COP times an efficiency factor; or simulate the cycle.
5. Integrate with pinch analysis to minimise refrigeration load.

## Gotchas
- Refrigerant regulation and phase-out schedules change; confirm current rules for the jurisdiction.
- Ammonia is toxic; flammable refrigerants need hazardous area review.

## Verify
- [ ] Load by level sums to compressor duty plus heat rejection.
- [ ] Compressor ratio per stage is within the machine limit.
