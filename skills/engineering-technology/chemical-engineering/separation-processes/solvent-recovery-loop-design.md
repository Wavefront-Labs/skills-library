---
id: engineering-technology.chemical-engineering.separation-processes.solvent-recovery-loop-design
name: solvent-recovery-loop-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-liquid-extraction, solvent-recovery-loop-design, solvent-recovery, extraction-loop, desolventizing, solvent-makeup, solvent-loss, recycle-loop, extract-distillation, stripping-raffinate]
level: practitioner
status: draft
description: "Design the solvent recovery loop around an extractor: raffinate and extract desolventising, make-up, losses, impurity build-up and energy integration."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Solvent recovery loop design

**Goal:** a closed solvent loop that meets product purity with acceptable losses and energy.

## Loop elements
1. **Extract desolventising**: distillation, evaporation or flash to separate solvent from solute; the solvent is returned to the extractor.
2. **Raffinate polishing**: stripping or distillation to remove dissolved solvent before disposal or the next step (solvent solubility in the raffinate drives losses).
3. **Make-up** for losses (solubility, entrainment, vent, degradation).
4. **Purge** to prevent accumulation of heavy impurities and water.
5. **Decanter** for water-solvent systems; reflux drum behaviour.

## Procedure
1. Compute the extract and raffinate compositions from the extraction calculation.
2. Choose recovery technology by relative volatility and thermal stability (see column skills).
3. Close the recycle in the flowsheet simulator; include make-up and purge, identify tear streams.
4. Check solvent purity in the recycle (water, solute), which feeds back into extractor performance.
5. Energy integrate: preheat the extract feed with recovered solvent; evaluate multi-effect or vapour recompression for large duties.
6. Estimate losses per tonne of product and the annual make-up cost and emissions.

## Gotchas
- Small impurity accumulation can ruin selectivity after weeks of operation; design the purge.
- Solvent loss to wastewater needs treatment or recovery.
- Flammable or toxic solvents add inventory and emission limits; confirm applicable regulations.

## Verify
- [ ] Loop mass balance closes at steady state including make-up and purge.
- [ ] Solvent loss target met in the model with a margin.
