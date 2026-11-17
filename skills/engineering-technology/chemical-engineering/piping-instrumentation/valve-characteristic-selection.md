---
id: engineering-technology.chemical-engineering.piping-instrumentation.valve-characteristic-selection
name: valve-characteristic-selection
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-control-valve-sizing, valve-characteristic-selection, valve-characteristic, equal-percentage, linear-valve, quick-opening, installed-characteristic, valve-authority, valve-gain, control-valve]
level: practitioner
status: gated
description: "Choose valve inherent characteristic (linear, equal percentage, quick opening) from the installed gain: valve authority, process gain variation and loop stability."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
  - "https://www.emerson.com/documents/automation/control-valve-handbook-en-3661206.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Valve characteristic selection

**Goal:** a valve whose installed characteristic gives a roughly constant loop gain over the operating range.

## Inherent characteristics
- **Linear**: flow proportional to travel; constant gain.
- **Equal percentage**: equal change in flow per equal change in travel; gain increases with opening; nominal rangeability about 50:1 (gated: unconfirmed, source is paywalled or blocked).
- **Quick opening**: large flow at small opening; used for on-off or relief type duty, not modulating control.

## Installed characteristic
The valve is in series with the process. The system takes part of the pressure drop; valve authority a = dP_valve (at full open or design)/total system dP. High authority leaves the characteristic close to inherent; low authority distorts it (the numeric authority thresholds in this skill, a > 0.5 and a < 0.25, are rules of thumb (gated: unconfirmed, source is paywalled or blocked)): a linear valve behaves like quick opening and an equal percentage valve moves toward linear.

## Selection rules
1. Use **equal percentage** where a large share of the pressure drop is absorbed by the system and only a small share is available at the valve (pressure control and highly varying pressure drop; the Emerson Control Valve Handbook gives this guidance), and where process gain falls with load.
2. Use **linear** for liquid level control and flow applications needing constant gain, with a large valve share of the pressure drop (about a > 0.5 is a rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
3. For gas pressure control or temperature control with heat exchangers, check the process gain curve: choose the valve characteristic that makes the product of the gains roughly constant.
4. Confirm by plotting installed flow against travel and computing the slope at minimum, normal and maximum.

## Gotchas
- Changing characteristic through the positioner cams or software characterisation is possible, but fix the root issue (authority) first.
- A valve running in the lowest 10% of travel is hard to control with any characteristic.

## Verify
- [ ] Installed loop gain varies by no more than about 4:1 across the working range (the guideline in the Emerson Control Valve Handbook, from the EnTech specification), or tuning is scheduled.
- [ ] Authority stated per valve.
