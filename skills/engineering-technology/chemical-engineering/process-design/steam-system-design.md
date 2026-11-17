---
id: engineering-technology.chemical-engineering.process-design.steam-system-design
name: steam-system-design
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-utilities-and-offsites, steam-system-design, steam-system, steam-levels, condensate-return]
level: practitioner
status: draft
description: "Lay out plant steam levels, letdown and condensate return, and size the boiler and header basis for a process plant."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Steam system design

**Goal:** Lay out plant steam levels, letdown and condensate return, and size the boiler and header basis for a process plant.

## Steps
1. Pick steam levels (for example high, medium and low pressure headers) from process temperature needs plus a driving force; saturation temperature at the header must exceed the process temperature by the approach.
2. Tabulate steam consumers and producers by level to get net header balances; size letdown stations and vent for imbalances.
3. Size boiler capacity for the peak demand plus margin, and allow for blowdown and deaerator steam.
4. Plan condensate return and recovery (flash steam from high-pressure condensate to a lower header) and treat it for contamination risk.
5. Prefer back-pressure turbine drives where mechanical power is also needed, if the economics support it.

## Gotchas
- Steam pressures and levels vary between sites; follow the site standard.
- Superheat and desuperheater needs depend on the turbine and process.

## Verify
- [ ] Each header balances at normal, minimum and maximum cases.
- [ ] Condensate return fraction is stated and justified.
