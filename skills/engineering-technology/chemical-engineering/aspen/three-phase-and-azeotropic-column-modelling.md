---
id: engineering-technology.chemical-engineering.aspen.three-phase-and-azeotropic-column-modelling
name: three-phase-and-azeotropic-column-modelling
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-column-simulation, three-phase-and-azeotropic-column-modelling, three-phase-distillation, azeotropic-distillation, decanter, radfrac, vle-lle, entrainer, aspen-plus, heterogeneous]
level: advanced
status: draft
description: "Model heterogeneous azeotropic and three-phase distillation in RadFrac with decanter, valid phases, key components and the initial estimates that make it converge."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three-phase and azeotropic column modelling

**Goal:** a converged heterogeneous azeotropic column (for example, dehydration with an entrainer) with the decanter modelled.

## Steps
1. **Property method and data**: an activity model with VLE and LLE binaries; check that the model predicts the liquid split in the decanter (Property Analysis ternary diagram).
2. **RadFrac configuration**: Valid phases = Vapor-Liquid-Liquid; convergence = Azeotropic (or strongly non-ideal option available in your version); list key components that form the second liquid.
3. **Decanter**: either the condenser as a decanter (the second-liquid stream returned as reflux or sent to another block) or a separate Decanter block; specify temperature and split assumptions.
4. **Entrainer loop**: close the recycle with a make-up stream; set a tear on the entrainer loop.
5. **Initial estimates**: start with two-phase (V-L) and moderate non-ideality, then enable three-phase; supply composition estimates for the aqueous and organic phases.
6. **Spec**: start with reflux and distillate rate, then move to purity design specs.
7. Verify the liquid-liquid split on specific trays and the decanter temperature.

## Gotchas
- Three-phase calculations multiply the failure modes: a tray that flips between one and two liquid phases causes oscillation.
- Models can predict a second liquid phase on trays that do not have one in practice (or vice versa); check against data.
- Relief and operating-envelope behaviour of such columns is sensitive to water inventory; do not rely only on steady-state simulation.

## Verify
- [ ] Liquid-liquid split compositions agree with LLE data.
- [ ] Entrainer make-up is small and steady; loop closure error is small.
