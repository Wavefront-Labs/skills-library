---
id: engineering-technology.chemical-engineering.aspen.simulator-to-pinch-data-extraction
name: simulator-to-pinch-data-extraction
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-heat-transfer-and-utilities-blocks, simulator-to-pinch-data-extraction, pinch-data-extraction, stream-data, energy-analysis]
level: practitioner
status: draft
description: "Extract hot and cold stream data (supply and target temperatures, heat capacity flowrate) from an Aspen model for pinch analysis."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Simulator to pinch data extraction

**Goal:** Extract hot and cold stream data (supply and target temperatures, heat capacity flowrate) from an Aspen model for pinch analysis.

## Steps
1. Identify each process stream that needs heating or cooling (heaters, coolers, reboilers, condensers and exchanger sides).
2. Record supply and target temperature and duty for each; compute CP = duty / (T_supply - T_target) for sensible streams.
3. For phase-change streams, split into segments (sensible heating, boiling, superheating) so each has near-constant CP.
4. Use the stream heat curves to linearise nonlinear segments.
5. Use AspenTech energy analysis tools if licensed, or export to a spreadsheet and build composite curves there.

## Gotchas
- Do not include utility streams as process streams.
- Apply the minimum approach temperature consistently when shifting temperatures.

## Verify
- [ ] Total hot and cold duties match the flowsheet energy balance.
- [ ] Stream data are consistent with the heat curves.
