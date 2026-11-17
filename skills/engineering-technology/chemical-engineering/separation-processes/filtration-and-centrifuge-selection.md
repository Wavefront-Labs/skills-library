---
id: engineering-technology.chemical-engineering.separation-processes.filtration-and-centrifuge-selection
name: filtration-and-centrifuge-selection
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-solid-liquid-and-gas-solid, filtration-and-centrifuge-selection, filtration, centrifuge, cake-filtration, equipment-selection]
level: practitioner
status: draft
description: "Select a filter or centrifuge from slurry tests (settling rate, cake permeability, solids content) and apply the constant-pressure cake filtration equation."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filtration and centrifuge selection

**Goal:** Select a filter or centrifuge from slurry tests (settling rate, cake permeability, solids content) and apply the constant-pressure cake filtration equation.

## Steps
1. Characterise the slurry: solids concentration, particle size, settling rate, cake compressibility and the need for cake washing.
2. Constant-pressure cake filtration: t/V = (mu alpha c / (2 A^2 delta P)) V + (mu R_m / (A delta P)); a plot of t/V versus V gives the cake resistance from the slope and the medium resistance from the intercept.
3. Use a selection chart: fast-settling coarse solids go to decanter or pusher centrifuges and vacuum belts; fine slow-settling solids go to pressure filters or membrane presses.
4. Check the washing, the dryness and the discharge needs; confirm with the vendor and the lab or pilot tests.
5. Size the area for the filtrate rate with a cycle time.

## Gotchas
- Lab tests need the actual slurry; cake properties vary with the particle size and the temperature.
- Cake compressibility makes the resistance depend on pressure.

## Verify
- [ ] Linear t/V versus V plot.
- [ ] Selected equipment passes the vendor test.
