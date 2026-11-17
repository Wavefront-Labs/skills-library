---
id: engineering-technology.chemical-engineering.separation-processes.pressure-swing-distillation
name: pressure-swing-distillation
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-special-distillation, pressure-swing-distillation, pressure-swing-distillation, azeotrope-shift, two-column-system]
level: practitioner
status: draft
description: "Design pressure-swing distillation for pressure-sensitive azeotropes using two columns at different pressures."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pressure swing distillation

**Goal:** Design pressure-swing distillation for pressure-sensitive azeotropes using two columns at different pressures.

## Steps
1. Check that the azeotrope composition changes appreciably with pressure (compute it at two pressures from the VLE model).
2. Feed a column at pressure 1 that yields pure A as one product and the azeotrope at its composition as the other.
3. Send that azeotrope to a column at pressure 2 where the azeotrope lies on the other side so pure B is produced and the azeotrope is recycled.
4. Use heat integration (the condenser of the high-pressure column drives the reboiler of the other) to save energy.
5. Check recycle size, which can be large if the shift is small.

## Gotchas
- A small azeotrope shift gives a large recycle and an expensive design.
- Temperature limits for the thermal stability of the components.

## Verify
- [ ] Azeotrope compositions at both pressures are computed from validated data.
- [ ] Recycle ratio is acceptable.
