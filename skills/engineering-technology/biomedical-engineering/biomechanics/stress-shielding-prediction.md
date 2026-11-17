---
id: engineering-technology.biomedical-engineering.biomechanics.stress-shielding-prediction
name: stress-shielding-prediction
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [stress-shielding, femoral-stem, bone-loss, implant-stiffness, remodeling-simulation]
level: advanced
status: draft
description: "Predict stress shielding around orthopaedic implants with FEA: strain energy versus intact bone, stiffness effects, remodelling simulation and validation against density data."
sources: ["Huiskes, Weinans and van Rietbergen, The relationship between stress shielding and bone resorption around total hip stems (Clin Orthop Relat Res, 1992)", "Engh and Bobyn literature on stem stiffness and bone loss (confirm citations)", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Stress shielding prediction

**Goal:** estimate how much load an implant carries away from bone, and where bone loss is likely.

## Mechanism
- A stiff implant bonded or fitted to bone carries much of the load, reducing the stimulus in adjacent bone, which then loses density over time (see bone-remodeling).
- Stiffness of a stem section scales with material modulus and the section's second moment of area; diameter has a strong effect (roughly fourth power for solid round sections). A fully porous or bonded interface increases shielding relative to a smooth, partially bonded one.

## Method
1. Build FE models of the intact bone and implanted bone with the same loads (hip joint force plus abductor force at representative load cases).
2. Compare strain energy density (SED) or strain in bone regions of interest (for example Gruen zones around a stem) between implanted and intact models; use the ratio as a stimulus change indicator. A large drop (for example below a stated fraction of intact) suggests resorption risk.
3. Optionally run a remodelling simulation to predict final density maps.
4. Compare designs: lower modulus materials, hollow or tapered stems, partial coating, shorter stems.
5. Validate against longitudinal DXA or CT bone density studies of similar implants, not only against bench strain gauges.

## Verify
- [ ] Interface assumption (bonded or partial) justified.
- [ ] Load cases cover multiple activities.
- [ ] Prediction compared with clinical bone density literature.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
