---
id: engineering-technology.chemical-engineering.aspen.reactive-distillation-modelling
name: reactive-distillation-modelling
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-column-simulation, reactive-distillation-modelling, reactive-distillation, radfrac, reactive-stages, kinetic-reaction, etbe, mtbe, esterification, aspen-plus, holdup]
level: advanced
status: gated
description: "Model reactive distillation in RadFrac: reactive stages, holdup, kinetic vs equilibrium reactions, catalyst loading and the checks that expose bad column assumptions."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reactive distillation modelling

**Goal:** a RadFrac model with reaction on selected stages that reproduces a realistic conversion and separation.

## Steps
1. (The study guide confirms RadFrac can model reactions via a Reaction ID; stage-range, holdup and menu details below are unconfirmed (gated: unconfirmed, source is paywalled or blocked).) Define the reaction set (Reactions > Reactions): equilibrium (K from Gibbs energy or user expression) or kinetic (power law or LHHW) in the liquid phase. Check the reaction rate basis: per volume of liquid, per mass of catalyst or per stage holdup.
2. In RadFrac, add the **Reactions** specification, choose the reaction ID, and give the **reactive stage range** (start and end stages).
3. Specify holdup for each reactive stage (liquid volume or residence time) or catalyst mass; kinetics need it.
4. Start with a non-reactive column that converges, then switch on reactions with an equilibrium reaction (easier), then change to kinetic.
5. Check thermodynamics: reactive mixtures often are strongly non-ideal (esterifications, etherifications); validate the property method with VLE and, if relevant, LLE data first.
6. Inspect profiles: conversion by stage, temperature in the reactive section, and flows leaving the zone.
7. Reconcile with a separate reactor-plus-column flowsheet to see the benefit.

## Gotchas
- Kinetic reactive columns are sensitive to holdup assumptions; a value copied from another tower can invalidate the study.
- Reaction near an azeotrope or heterogeneous region may need three-phase calculations.
- Trays versus packed column hold-up and catalyst packing impose hardware limits not seen in the model.

## Verify
- [ ] Mass and atom balances close including the reaction.
- [ ] Conversion within the range expected from published or pilot data.
- [ ] Sensitivity to holdup and reflux shown.
