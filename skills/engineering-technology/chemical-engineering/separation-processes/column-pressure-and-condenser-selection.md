---
id: engineering-technology.chemical-engineering.separation-processes.column-pressure-and-condenser-selection
name: column-pressure-and-condenser-selection
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-column-hydraulics, column-pressure-and-condenser-selection, column-pressure, condenser-type, total-condenser, partial-condenser, vacuum-distillation, refrigerated-condenser, reflux-drum, reboiler-temperature]
level: practitioner
status: draft
description: "Choose distillation column operating pressure and condenser type from cooling-medium temperature, thermal stability, relative volatility and reboiler utility limits."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Column pressure and condenser selection

**Goal:** an operating pressure at which the column can use economical utilities and stay thermally safe.

## Method
1. Start at near-atmospheric pressure.
2. Check the **distillate bubble point** at that pressure. The condenser needs a temperature driving force to the coolant: with cooling water supplied around 30 C and returned near 40 C, the reflux drum temperature is often kept above roughly 45 to 50 C (a minimum approach of about 10 to 15 K). If the bubble point is lower, increase column pressure until it is acceptable.
3. Check the **bottoms temperature** at the chosen pressure. It must be below the thermal-stability limit of the product and below the available heating medium temperature less approach (for example for 4 barg steam about 150 C saturation; confirm your steam levels). If the bottoms temperature is too high, reduce pressure (vacuum).
4. If both conflict, consider refrigerated condensing, a different heat source (hot oil), or another separation method.
5. **Relative volatility increases at lower pressure** for most systems; lower pressure reduces stage count but requires larger diameter and vacuum equipment.

## Condenser types
- **Total condenser**: all vapour condensed; reflux and distillate are liquid at the same composition.
- **Partial condenser**: vapour distillate or vent for noncondensables (the condenser acts as an equilibrium stage); needed when light noncondensable gases are present or product is vapour.
- **Dephlegmator** (reflux condenser integrated in the column) and **refrigerated** options for low-boiling distillates.

## Gotchas
- Pressure also changes azeotrope composition.
- Column pressure set by design must stay inside the relief design pressure ratings.
- Pressure drop across the condenser raises the actual column top pressure.

## Verify
- [ ] Top and bottom temperatures computed at final pressure with utilities approach temperature margins.
- [ ] Condenser type justified with noncondensable and product-phase requirements.
