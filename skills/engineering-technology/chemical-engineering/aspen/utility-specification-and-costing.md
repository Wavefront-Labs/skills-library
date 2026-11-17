---
id: engineering-technology.chemical-engineering.aspen.utility-specification-and-costing
name: utility-specification-and-costing
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-heat-transfer-and-utilities-blocks, utility-specification-and-costing, utilities, utility-costing, energy-cost]
level: practitioner
status: draft
description: "Define utilities in Aspen Plus (steam, cooling water, fuel) and use them to cost each heater and cooler in the simulation."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Utility specification and costing

**Goal:** Define utilities in Aspen Plus (steam, cooling water, fuel) and use them to cost each heater and cooler in the simulation.

## Steps
1. Create utility definitions: type (heating or cooling), inlet and outlet conditions, and price per energy or mass unit.
2. Assign the utility to each heater or cooler block; Aspen calculates utility flow and cost per block.
3. Check outlet temperatures are consistent with real utility levels (steam pressure, cooling water return limit).
4. Report totals from the utilities summary for operating cost and energy targeting.
5. Use a consistent price basis and record the year and source of prices.

## Gotchas
- Utility prices are site and time specific; do not reuse generic values without confirmation.
- Cooling water return temperature limits depend on water quality.

## Verify
- [ ] Block-level duties sum to the utility totals.
- [ ] Cost totals match a hand estimate.
