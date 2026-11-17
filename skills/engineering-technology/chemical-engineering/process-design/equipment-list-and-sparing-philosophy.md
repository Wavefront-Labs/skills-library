---
id: engineering-technology.chemical-engineering.process-design.equipment-list-and-sparing-philosophy
name: equipment-list-and-sparing-philosophy
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-design-basis-and-pfd, equipment-list-and-sparing-philosophy, equipment-list, sparing, spare-pumps, reliability, availability, redundancy, 2x100, n-plus-1, maintenance-philosophy]
level: practitioner
status: draft
description: "Build the equipment list and decide sparing (N+1, 2x100%, 2x50%) from criticality, failure rates, maintenance and economics, and write it down."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Equipment list and sparing philosophy

**Goal:** a complete equipment list with a defensible redundancy decision for each rotating or critical item.

## Equipment list
One line per item: tag, service, type, number of units (operating plus spare), key sizing data (duty, flow, head, design pressure and temperature), materials of construction, driver and power, preliminary weight, and the source drawing. Produce it from the PFD; update after each simulation revision.

## Sparing rules of thumb
| Item | Common arrangement |
|---|---|
| Process pumps | One operating, one installed spare (1+1) for continuous critical service; shared spare for several similar services |
| Large compressor | Often single unit with maintenance plan; a spare only if production loss is high |
| Heat exchangers, vessels, columns | Usually not spared; plan cleaning bypasses for fouling duties |
| Filters and strainers | Duplex (two in parallel) if continuous service |
| Control valves | Bypass and block valves for maintenance only when plant cannot stop |

## Decision method
1. Estimate the cost of lost production per day.
2. Estimate the failure rate and repair time for the equipment (plant history or vendor data).
3. Compare the annual cost of lost production with the cost of the spare plus installation.
4. Consider simultaneous maintenance needs (seal changes, strainer cleaning) and safety function (cooling pump failure leading to unsafe state).

## Gotchas
- A spare on the same power supply and same switchgear does not protect against power loss.
- Spare pumps that are never run seize; plan periodic rotation.
- Sparing decisions drive layout and piping; make them early.

## Verify
- [ ] Every sparing choice has a recorded reason.
- [ ] Equipment list reconciles with PFD and simulation.
