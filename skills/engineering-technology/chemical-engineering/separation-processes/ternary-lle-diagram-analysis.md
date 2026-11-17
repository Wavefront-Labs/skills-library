---
id: engineering-technology.chemical-engineering.separation-processes.ternary-lle-diagram-analysis
name: ternary-lle-diagram-analysis
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-liquid-extraction, ternary-lle-diagram-analysis, ternary-diagram, lle, tie-line, plait-point, lever-rule, distribution-coefficient, selectivity, liquid-liquid-extraction, triangular-diagram]
level: practitioner
status: draft
description: "Read and use ternary liquid-liquid equilibrium diagrams: lever rule, tie lines, plait point, distribution coefficient and selectivity for solvent choice."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ternary LLE diagram analysis

**Goal:** use the ternary diagram to judge a solvent and set up extraction calculations.

## Reading the diagram
- Equilateral triangle: corners A (solute), C (carrier), S (solvent); a point's composition is read from distances to the sides; mass fractions are common.
- **Binodal curve** separates the single-phase region from the two-phase region; a mixture point inside splits into the extract (solvent-rich) and raffinate (carrier-rich) phases at the ends of the **tie line** through it.
- **Lever rule**: M x (distance to raffinate) ... the ratio of extract mass to raffinate mass equals the distance from the mixture point to the raffinate end divided by the distance to the extract end.
- **Plait point**: where tie lines shrink to zero length.

## Quantities
- Distribution coefficient K = y_A/x_A (extract over raffinate mass fraction of solute).
- Selectivity beta = (y_A/y_C)/(x_A/x_C); beta above 1 is needed; larger is better (typical wanted > 2 to 3 for practical extraction).
- Solvent mutual solubility with the carrier should be low.

## Steps
1. Obtain LLE data or fit a model (see NRTL skills) and plot the diagram with tie lines.
2. Locate feed F and solvent S; mixture point M on line FS by the lever rule (M = F + S).
3. Draw the tie line through M (interpolate between the data tie lines) to get extract and raffinate.
4. Compute the single-stage recovery; judge whether many stages are needed.
5. Check the **minimum solvent** (mixture on the binodal: the maximum possible dilution) and maximum solvent.

## Gotchas
- Temperature dependence can be strong; plot at the operating temperature.
- Mass vs mole fractions: use one basis consistently.

## Verify
- [ ] Mass balance: F + S = E + R and solute balance holds from the diagram.
- [ ] Tie lines consistent with measured data.
