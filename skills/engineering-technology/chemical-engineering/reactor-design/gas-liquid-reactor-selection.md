---
id: engineering-technology.chemical-engineering.reactor-design.gas-liquid-reactor-selection
name: gas-liquid-reactor-selection
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-multiphase-reactors, gas-liquid-reactor-selection, gas-liquid-reactor, reactor-selection, hatta-number]
level: practitioner
status: draft
description: "Select a gas-liquid reactor type (stirred tank, bubble column, packed column, loop) from the reaction regime and mass transfer needs."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gas liquid reactor selection

**Goal:** Select a gas-liquid reactor type (stirred tank, bubble column, packed column, loop) from the reaction regime and mass transfer needs.

## Steps
1. Classify the reaction regime with the Hatta number Ha = sqrt(k D_A) / k_L (for a first-order reaction in the liquid film): Ha well below 0.3 means slow reaction (bulk liquid reaction controls), above 3 means fast reaction in the film; confirm limits with a text.
2. Slow reactions need liquid volume (bubble column or stirred tank); fast reactions need interfacial area (packed column, spray, or stirred tank at high power).
3. Compare reactors by kLa and gas holdup ranges and heat removal needs.
4. Check the gas solubility, pressure and safety (oxygen in flammable liquid).
5. Choose with a preliminary cost and scale-up risk assessment.

## Gotchas
- Selection also depends on solids, fouling and corrosion.
- Mass transfer data should be confirmed experimentally.

## Verify
- [ ] Regime is stated with the supporting estimates.
- [ ] Selected reactor gives the needed kLa or area.
