---
id: engineering-technology.chemical-engineering.process-design.heat-and-material-balance-sheet
name: heat-and-material-balance-sheet
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-design-basis-and-pfd, heat-and-material-balance-sheet, heat-and-material-balance, hmb, handover, stream-data, design-cases, turndown, balance-sheet, project-deliverable]
level: practitioner
status: draft
description: "Prepare the heat and material balance sheet used for handover: scope, cases, units, basis and checks so process, mechanical and operations teams share one set of numbers."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Heat and material balance sheet for handover

**Goal:** a controlled deliverable (spreadsheet or drawing-format table) that every discipline can use to size equipment.

## Structure
1. **Cases**: normal design, maximum (design margin), turndown, start-up, and any alternative feeds.
2. **Per stream**: number, description, phase, flows (kg/h, kmol/h), composition, T, P, enthalpy, density, viscosity, thermal conductivity and other properties required by sizing.
3. **Per unit**: duties, heat of reaction, utility rates, power.
4. **Summary page**: overall balance, utilities summary, yields and losses, specific consumption (per tonne of product).
5. **Revision control**: revision, date, simulation file name and version.

## How to produce
Export from the simulator to a spreadsheet with a macro or script, add checks columns (mass, element, energy), freeze the basis. Do not retype.

## Checks
- Overall in = out for mass within 0.1%.
- Every unit's energy balance closes within simulation tolerance.
- Utilities in the summary match sums over units.
- Normal case rates against design basis targets.

## Gotchas
- Properties differ between simulator and the vendor data sheet; note which source drives which design.
- Sizing at maximum case but pricing at normal case needs both on the sheet.
- Start-up and upset cases are often missing and control the relief or pump selection.

## Verify
- [ ] Revision history is current; changes since last issue flagged.
- [ ] A reviewer other than the author recomputed one unit by hand.
