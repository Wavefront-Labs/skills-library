---
id: engineering-technology.chemical-engineering.process-design.plant-air-nitrogen-fuel-gas-utilities
name: plant-air-nitrogen-fuel-gas-utilities
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-utilities-and-offsites, plant-air-nitrogen-fuel-gas-utilities, plant-air, instrument-air, nitrogen, fuel-gas]
level: practitioner
status: draft
description: "Size plant and instrument air, nitrogen and fuel gas utilities from consumer lists, with dryers, storage and backup basis."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plant air nitrogen fuel gas utilities

**Goal:** Size plant and instrument air, nitrogen and fuel gas utilities from consumer lists, with dryers, storage and backup basis.

## Steps
1. Build consumer lists: instrument air, plant air, nitrogen (purge, blanketing, inerting) and fuel gas (heaters, flare pilots).
2. Add a diversity factor to the sum for peak demand and leakage allowance; document the basis.
3. Instrument air needs drying to a dew point suitable for the coldest site temperature; size receivers for ride-through on compressor failure.
4. Nitrogen: choose between liquid storage and vaporisers or on-site generation (membrane or PSA) from purity and flow; specify purity for oxygen-sensitive duty.
5. Fuel gas: set pressure, knockout and heating value variation; check supply security and flare gas recovery interaction.

## Gotchas
- Instrument air loss usually drives fail-safe valve action; check the backup basis.
- Nitrogen is an asphyxiant; confined space and vent location need review.

## Verify
- [ ] Peak demand covers the largest transient.
- [ ] Receiver volume provides the required ride-through time.
