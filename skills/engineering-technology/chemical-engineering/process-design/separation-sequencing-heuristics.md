---
id: engineering-technology.chemical-engineering.process-design.separation-sequencing-heuristics
name: separation-sequencing-heuristics
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-flowsheet-synthesis, separation-sequencing-heuristics, separation-sequencing, sequencing-heuristics, distillation-sequence, direct-sequence, indirect-sequence, column-sequence, synthesis]
level: practitioner
status: draft
description: "Apply separation sequencing heuristics (remove corrosives first, most plentiful first, favour equimolar splits, hardest last) and test the top sequences by cost."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Separation sequencing heuristics

**Goal:** a short list of promising separation sequences, then a cost comparison.

## Commonly used heuristics
1. Remove corrosive, hazardous or reactive components early.
2. Remove the most plentiful component first (reduces load downstream).
3. Favour near 50/50 splits of molar flow between top and bottom.
4. Perform the difficult separation (low relative volatility, close boilers) last, when flows are smallest and when purity is high.
5. Avoid vacuum and refrigeration where possible; prefer lower-cost utilities.
6. Prefer direct sequence (light component first) unless another heuristic overrides.
7. Separate by the least costly method where properties permit (flash, decantation, then distillation).

## Method
1. Choose the splits that satisfy the heuristics; count sequences (for N products there are many; for 4 components the number of simple-column sequences is 5).
2. Estimate each column with shortcut design (reflux, stage count, vapour rate); cost with cost correlations.
3. Include side effects: heat integration opportunities, different pressures, product purity.
4. Compare total annualised cost; verify top two in a rigorous model.

## Gotchas
- Heuristics conflict; the cost estimate decides.
- Heat integration can change the ranking; evaluate with pinch (see `engineering-technology.chemical-engineering.heat-exchanger-design.composite-curves-and-pinch-targets`).
- Azeotropes break simple sequencing; use residue curve analysis first.

## Verify
- [ ] Shortlist justified by heuristics and by costs.
- [ ] Rigorous simulation of finalists.
