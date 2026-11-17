---
id: engineering-technology.chemical-engineering.aspen.hysys-spreadsheet-and-adjust-logic
name: hysys-spreadsheet-and-adjust-logic
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-sensitivity-and-optimisation, hysys-spreadsheet-and-adjust-logic, hysys-spreadsheet, adjust-operation, set-operation]
level: practitioner
status: draft
description: "Use the HYSYS Spreadsheet, Adjust and Set operations to implement calculations and targets, with sensible bounds and order."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hysys spreadsheet and adjust logic

**Goal:** Use the HYSYS Spreadsheet, Adjust and Set operations to implement calculations and targets, with sensible bounds and order.

## Steps
1. Use the Spreadsheet to import variables, compute derived values (ratios, costs, KPIs) and export results back to streams or operations.
2. Use the Adjust operation to vary one variable until a target is met; set tolerance, step size and maximum iterations.
3. Use the Set operation for simple linear links between two variables (multiplier and offset).
4. Keep each adjusted variable linked to one target; use the spreadsheet for multi-variable logic.
5. Watch recycle interactions: an Adjust inside a recycle loop may need larger tolerances or an outer Adjust sequence.

## Gotchas
- Unbounded Adjust steps can wander into infeasible conditions.
- Document spreadsheet cell meanings; they are easy to lose.

## Verify
- [ ] Target is met within tolerance.
- [ ] No cells show error values.
