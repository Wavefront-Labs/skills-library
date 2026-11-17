---
id: engineering-technology.chemical-engineering.process-design.hierarchical-decision-procedure
name: hierarchical-decision-procedure
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-flowsheet-synthesis, hierarchical-decision-procedure, douglas-hierarchy, conceptual-design, economic-potential, flowsheet-synthesis, batch-vs-continuous]
level: practitioner
status: draft
description: "Apply Douglas's hierarchical procedure to synthesise a flowsheet in levels, with an economic-potential check at each level, then stop when the potential is negative."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Douglas hierarchical decision procedure

**Goal:** a conceptual flowsheet built level by level with early economics, so ideas that cannot pay are dropped before simulation effort.

## The levels
1. **Batch versus continuous**: decide from production scale, product value, kinetics and flexibility; large commodity processes are continuous.
2. **Input-output structure**: list feeds, products, by-products; set purge and recycle needs; compute the first economic potential EP1 = product value minus raw material cost.
3. **Recycle structure and reactor**: number of reactors, recycles, need for gas compressor, heat effects; adjust EP to subtract the cost of the reactor system and recycle.
4. **Separation system**: vapour recovery and liquid separation; choose units (flash, distillation, absorption, membrane); use sequencing heuristics.
5. **Heat-exchanger network**: pinch targets and design.

## Method
At each level compute a short-cut economic potential (revenue minus operating cost minus annualised capital) with order-of-magnitude costs. If EP at a level is negative and cannot be rescued by a plausible improvement, stop or revise earlier decisions.

## Practice
- Keep a decision log: alternatives, quantitative reason for the choice, owner.
- Revisit earlier levels when later ones expose large costs (for example, an expensive separation can justify a different reactor conversion).

## Gotchas
- Doing everything in a simulator too early hides the main trade-offs.
- Utilities and waste treatment costs are often forgotten at level 2 and sink the project later.

## Verify
- [ ] Decision log with an economic number at each level.
- [ ] A negative-EP alternative was explicitly discarded.
