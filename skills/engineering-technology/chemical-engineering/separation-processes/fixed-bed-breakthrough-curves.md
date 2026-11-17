---
id: engineering-technology.chemical-engineering.separation-processes.fixed-bed-breakthrough-curves
name: fixed-bed-breakthrough-curves
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-adsorption-and-ion-exchange, fixed-bed-breakthrough-curves, breakthrough-curve, mass-transfer-zone, fixed-bed-adsorption]
level: practitioner
status: draft
description: "Analyse a fixed-bed breakthrough curve: mass transfer zone, bed length and the length of unused bed approach."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fixed bed breakthrough curves

**Goal:** Analyse a fixed-bed breakthrough curve: mass transfer zone, bed length and the length of unused bed approach.

## Steps
1. Obtain the breakthrough curve C/C0 versus time from a column test (feed concentration C0, flow, bed length).
2. Stoichiometric time t_st = integral of (1 - C/C0) dt (area above the curve); it gives the equilibrium capacity used.
3. Length of unused bed LUB = L (1 - t_b / t_st), where t_b is the breakthrough time at an agreed outlet concentration.
4. Design bed length = length for equilibrium capacity plus LUB; scale LUB with velocity and keep the same particle size.
5. Check pressure drop with Ergun and the regeneration time within the cycle.

## Gotchas
- LUB depends on velocity and particle size; keep these the same on scale-up.
- Fixed bed data from a short column can mislead; use a long enough bed.

## Verify
- [ ] Loading balance from the curve matches the isotherm capacity.
- [ ] Pressure drop is within limit.
