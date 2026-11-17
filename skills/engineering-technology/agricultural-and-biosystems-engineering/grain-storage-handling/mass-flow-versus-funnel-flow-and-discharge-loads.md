---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.mass-flow-versus-funnel-flow-and-discharge-loads
name: mass-flow-versus-funnel-flow-and-discharge-loads
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, mass-flow-funnel-flow, silo-loads, bin-structural-design, discharge-pressure, eccentric-discharge, rathole, jenike]
level: practitioner
status: verified
description: "Classify silo discharge as mass or funnel flow, recognise eccentric and dynamic loads, and avoid structural overload and ratholing from the wrong hopper and outlet."
sources:
  - "Sinha & Muir, Grain Storage: Part of a System"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Eurocodes, JRC (https://eurocodes.jrc.ec.europa.eu/EN-Eurocodes/eurocode-1-actions-structures)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mass flow versus funnel flow and discharge loads

**Goal:** predictable discharge and structural loads in storage and process bins.

## Flow patterns
- **Mass flow**: all material moves during discharge, first-in first-out; needs steep, smooth hoppers; wall pressures change abruptly at the hopper transition.
- **Funnel (core) flow**: a channel above the outlet flows while material at the walls stays stagnant (last-in first-out); typical of flat-bottom bins with a central outlet or sweep auger. Wet or cohesive material can form a rathole or arch.
- Jenike's method determines the hopper angle and minimum outlet from shear-cell measurement of the material's flow function and wall friction.

## Loads
1. Discharge increases wall pressure above static values, the overpressure depending on the flow pattern and bin geometry; the design code (EN 1991-4, Eurocode 1 Part 4: Silos and tanks, per the JRC Eurocodes site; ASABE EP433 (gated: unconfirmed, source is paywalled or blocked)) gives factors.
2. **Eccentric discharge** (outlets off-centre) causes unequal wall loads, bending and buckling risk; avoid off-centre outlets or design for them explicitly.
3. **Core flow with collapsing arch** produces impact loads and "silo quaking".
4. Emptying with vacuum or aeration changes pressures.

## Design practice
- Use symmetric centre discharge; keep multiple outlets operating in a sequence recommended by the designer.
- Provide inspection ports and monitoring for bridging in bins that handle fines.
- Wall materials (steel, concrete) affect friction.

## Gotchas
- Collapse of silos is often due to discharge overpressure on partly full bins or poor stiffening; do not alter outlets without engineering review.
- Entering a bin to break a bridge is a lethal hazard (see the engulfment skill).

## Verify
- [ ] Discharge test sequence is documented and structural review covers the chosen pattern.
