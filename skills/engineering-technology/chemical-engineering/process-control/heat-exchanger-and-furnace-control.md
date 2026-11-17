---
id: engineering-technology.chemical-engineering.process-control.heat-exchanger-and-furnace-control
name: heat-exchanger-and-furnace-control
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-unit-operation-control, heat-exchanger-and-furnace-control, heat-exchanger-control, furnace-control, bypass-control]
level: practitioner
status: gated
description: "Control heat exchangers and fired heaters: bypass and utility flow control, outlet temperature cascade and combustion safety."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
  - "https://www.nfpa.org/product/nfpa-86-standard-for-ovens-and-furnaces/p0086code"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heat exchanger and furnace control

**Goal:** Control heat exchangers and fired heaters: bypass and utility flow control, outlet temperature cascade and combustion safety.

## Steps
1. Control the outlet temperature by manipulating the utility flow, or a process bypass for the cases where the utility flow control gives poor response at low flow.
2. Use cascade from the process outlet temperature to the utility valve or the fuel pressure; use feedforward on the feed flow and temperature.
3. For fired heaters, add pass-balancing, excess air control from the oxygen and the draft pressure control; use cross-limiting between fuel and air.
4. Burner management and flame safety are separate safety systems per the applicable standard (NFPA 86 is the Standard for Ovens and Furnaces, which may not cover fired process heaters; EN 746 and heater codes such as API 556 or NFPA 87 may apply instead, confirm which applies (gated: unconfirmed, source is paywalled or blocked)). Combustion safety design needs a qualified engineer.
5. Check the nonlinear valve gain in steam duty and use equal percentage valves where appropriate.

## Gotchas
- Condensate backup in steam heaters causes unexpected dynamics.
- Burner safety systems are not part of the basic process control.

## Verify
- [ ] Controller responds across the load range.
- [ ] Combustion safety system is independent.
