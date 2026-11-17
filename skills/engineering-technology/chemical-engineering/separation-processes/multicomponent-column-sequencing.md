---
id: engineering-technology.chemical-engineering.separation-processes.multicomponent-column-sequencing
name: multicomponent-column-sequencing
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-special-distillation, multicomponent-column-sequencing, column-sequencing, multicomponent-distillation, dividing-wall-column]
level: practitioner
status: draft
description: "Sequence columns for multicomponent mixtures using heuristics, number of sequences and energy-saving thermally coupled options."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multicomponent column sequencing

**Goal:** Sequence columns for multicomponent mixtures using heuristics, number of sequences and energy-saving thermally coupled options.

## Steps
1. The number of sequences of simple columns for N products grows rapidly; for a three-product split there are two, and for four products there are five.
2. Apply heuristics: remove corrosive or hazardous components early, separate the most plentiful component or the easiest split first, and leave the difficult separation (close relative volatility) for last.
3. Consider side-draw columns, prefractionators and dividing wall columns when energy savings justify the complexity.
4. Evaluate the candidates by shortcut methods (Fenske, Underwood, Gilliland), then rigorous simulation for the best ones.
5. Compare using total annualised cost.

## Gotchas
- Heuristics sometimes conflict; evaluate numerically.
- Dividing wall columns need careful control and pressure matching.

## Verify
- [ ] Each sequence is costed on the same basis.
- [ ] Product purities are met in the rigorous simulation.
