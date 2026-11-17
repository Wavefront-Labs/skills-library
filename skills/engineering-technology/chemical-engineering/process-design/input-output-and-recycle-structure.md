---
id: engineering-technology.chemical-engineering.process-design.input-output-and-recycle-structure
name: input-output-and-recycle-structure
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-flowsheet-synthesis, input-output-and-recycle-structure, input-output-structure, recycle-structure, purge, excess-reactant, inert-accumulation, economic-potential, level-2-design]
level: practitioner
status: draft
description: "Set the input-output structure (feeds, products, purges, by-products) and the recycle structure, with excess-reactant, inert and purge decisions quantified."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input-output and recycle structure

**Goal:** fix which streams enter and leave the plant and which are recycled, with numbers.

## Input-output (level 2)
1. List every reaction, including by-product reactions, with reference conversions and selectivities.
2. Decide purification of feeds: impurity in the feed that is inert and accumulates, or poisons catalyst, must be removed or purged.
3. For each by-product, decide: recycle to extinction, sell, burn or dispose.
4. Compute EP1 = sum of product and by-product values minus feed costs.

## Recycle structure (level 3)
1. Choose recycle of unconverted reactants; consider excess of the cheaper reactant.
2. **Inert**: gas purge sized by F x z_inert = P x y_inert at the allowed loop concentration.
3. **Heat effects**: adiabatic temperature rise limits per-pass conversion; recycle can act as a diluent.
4. **Compressor**: gas recycle needs a recycle compressor; its cost trades against conversion.
5. Update economic potential: EP2 = EP1 minus reactor and compressor costs and raw material lost in the purge.

## Practice
Evaluate three or four candidate per-pass conversions and purge rates in a spreadsheet; plot EP versus conversion; choose near the maximum but consider flat optimum risk and safety margin.

## Gotchas
- Reactions that produce a heavy by-product that is not purged lead to accumulation; check each component for exit routes.
- Purging a valuable component without recovery is a classic loss.

## Verify
- [ ] Every component has an exit route (product, purge, vent or reaction).
- [ ] EP versus conversion plot saved.
