---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.mass-and-power-margin-philosophy
name: mass-and-power-margin-philosophy
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, systems-engineering, spacecraft-design, margin-philosophy, mass-growth-allowance, power-margin, contingency, budget-tracking]
level: practitioner
status: draft
description: "Set and track spacecraft mass and power margins by design maturity, using growth allowances, contingency and system margin, per AIAA S-120 style practice."
sources:
  - "AIAA S-120, Mass Properties Control for Space Systems"
  - "NASA Systems Engineering Handbook"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Mass and power margin philosophy

**Goal:** budgets that survive design growth.

## Concepts
- **Current best estimate (CBE):** the bottom-up number from the design as it stands.
- **Growth allowance (contingency):** added per component by maturity (a component off the shelf with flight heritage has a small allowance; a new design at concept stage carries a large one, often in the tens of percent, falling as design matures). Use the programme's table; AIAA S-120 is the common reference for mass.
- **Predicted = CBE + growth allowance.**
- **System-level margin:** held by the project above predicted mass or power against the launch vehicle or bus capability (for example 10-20% at Preliminary Design Review, with the schedule falling toward launch; exact numbers are programme-specific).
- Power: apply margin to loads in each mode and to the generation capability (end-of-life, worst-case conditions).

## Procedure
1. Build a budget spreadsheet: subsystem, component, CBE, maturity category, allowance, predicted, margin to capability.
2. Update at each design review; show the history so growth trends are visible.
3. Trigger descopes or design actions when margin falls below the schedule thresholds.
4. Track consumables (propellant) separately with the delta-v budget and its own margin.

## Gotchas
- Applying the same flat percentage to everything hides risk in immature items.
- Margin consumed by late requirement changes should be logged as such.

## Verify
- [ ] The budget reproduces from component data and shows margin vs the project's required schedule at the current milestone.
