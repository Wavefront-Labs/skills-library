---
id: engineering-technology.chemical-engineering.separation-processes.solubility-and-supersaturation
name: solubility-and-supersaturation
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-crystallisation-drying-evaporation, solubility-and-supersaturation, solubility-curve, supersaturation, metastable-zone-width, cooling-crystallization, antisolvent-crystallization, evaporative-crystallization, nucleation, yield]
level: practitioner
status: draft
description: "Build and use solubility curves, supersaturation ratio and metastable zone width to select a crystallisation method (cooling, evaporative, antisolvent) and operating window."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations, Mullin Crystallization"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Solubility curves and supersaturation

**Goal:** the thermodynamic basis for crystalliser design and the window in which crystals grow rather than nucleate wildly.

## Concepts
- **Solubility curve** C*(T): equilibrium concentration; measure by gravimetric or in-line methods at several temperatures (and solvent compositions for antisolvent).
- **Supersaturation** driving force: absolute DC = C - C*, ratio S = C/C*, or relative sigma = S - 1.
- **Metastable zone**: the region between solubility and the temperature or concentration where spontaneous (primary) nucleation occurs. Its width depends on cooling rate, agitation, impurities and seeding; measure it for your system.

## Method selection from the solubility curve
- **Steep curve** (solubility changes a lot with T): cooling crystallisation.
- **Flat curve**: evaporative crystallisation (remove solvent).
- **High solubility in solvent A but low in B**: antisolvent addition.
- Reactive (precipitation) crystallisation for sparingly soluble salts: very high supersaturation, fine particles.

## Yield estimate
For cooling from T1 to T2 with no solvent loss: yield = (C1 - C2*)/C1 mass per mass of solute fed (adjust for hydrates and solvent mass).

## Procedure
1. Measure or collect solubility data with a source and temperature range.
2. Determine the metastable zone width at the intended cooling rate (turbidity probe or similar).
3. Choose a seeded, controlled cooling or addition profile that stays inside the metastable zone.
4. Compute the yield and compare with spec.

## Gotchas
- Polymorphs and solvates have different solubility; confirm solid form.
- Impurities change solubility and habit.
- Unseeded batches give unpredictable nucleation.

## Verify
- [ ] Mass balance on solute and solvent for the yield.
- [ ] Operating line plotted against the solubility and metastable limits.
