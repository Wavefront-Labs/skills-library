---
id: engineering-technology.chemical-engineering.aspen.valve-and-pressure-drop-blocks
name: valve-and-pressure-drop-blocks
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-rotating-equipment-and-hydraulics, valve-and-pressure-drop-blocks, valve-block, pressure-drop-block, isenthalpic-flash]
level: practitioner
status: draft
description: "Model valves and pressure drops in Aspen Plus and HYSYS with Valve and Pipe blocks, including isenthalpic flash across the valve."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Valve and pressure drop blocks

**Goal:** Model valves and pressure drops in Aspen Plus and HYSYS with Valve and Pipe blocks, including isenthalpic flash across the valve.

## Steps
1. Use a Valve block with specified outlet pressure or pressure drop; the steady-state model assumes isenthalpic expansion.
2. Check for flashing across the valve: report vapour fraction and the temperature drop (Joule-Thomson effect).
3. Use the valve sizing option, where available, for Cv at design flow; confirm against vendor sizing.
4. Include pressure drops for filters, orifices and control valves so boundary conditions are realistic.
5. In HYSYS dynamic mode the valve uses Cv and position; set the valve characteristic correctly.

## Gotchas
- Cv from the simulator is preliminary; the instrument engineer or vendor sizes the purchased valve.
- Critical flow limits are checked separately.

## Verify
- [ ] Outlet vapour fraction and temperature are reasonable.
- [ ] Pressure drop matches the hydraulic basis.
