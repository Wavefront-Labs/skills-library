---
id: engineering-technology.chemical-engineering.aspen.rcstr-rplug-kinetic-models
name: rcstr-rplug-kinetic-models
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-reactor-blocks, rcstr-rplug-kinetic-models, rcstr, rplug, kinetic-reactor, residence-time, reaction-kinetics, aspen-plus, plug-flow, cstr]
level: practitioner
status: gated
description: "Set up RCSTR and RPlug in Aspen Plus with kinetic reactions: volume or residence time, phases, heat specifications and the typical convergence and units traps."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RCSTR and RPlug kinetic models

**Goal:** a kinetic reactor model whose outputs you can match to hand calculations.

## Steps
1. Define the **Reactions** object (type Power-law, LHHW or user) and assign it to the reactor.
2. (Reactor input names below are Aspen-specific (gated: unconfirmed, source is paywalled or blocked); the study guide confirms a Reaction ID with Power Law, Equilibrium, LHHW and Custom types drives kinetic reactors.) **RCSTR**: specify pressure and temperature (or duty), and either **volume** or **residence time**; set the reacting phase (liquid, vapor or both), and valid phases for the outlet flash.
3. **RPlug**: specify reactor type (specified temperature, adiabatic, constant coolant temperature, co-current/counter-current coolant), length and diameter (or tube number), and the pressure drop (specified or from the correlation).
4. **Check units**: power-law concentration basis (molarity, partial pressure, mole fraction), rate basis (reacting-phase volume, catalyst mass, or reactor volume); the kinetic parameters must match.
5. **Run**, then compare outlet conversion with a hand model (see `engineering-technology.chemical-engineering.reactor-design.pfr-design-and-integration`).
6. For RPlug, review the profile report (conversion and temperature along the length).

## Gotchas
- Rate constant units depend on concentration basis; a power-law k used in a different basis gives garbage but runs fine.
- RCSTR with a small volume and strongly exothermic reaction may have multiple steady states; the solver may pick the wrong branch. Start from a good temperature estimate.
- For adiabatic RPlug the energy balance requires accurate heat capacities and formation enthalpies.

## Verify
- [ ] A hand integral of the rate law (spreadsheet) matches the simulator to within a few percent.
- [ ] Temperature and conversion profiles are smooth and physically sensible.
