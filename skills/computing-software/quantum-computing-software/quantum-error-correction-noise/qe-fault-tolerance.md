---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-fault-tolerance
name: qe-fault-tolerance
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [fault-tolerance-magic-states]
level: sme
status: draft
description: "Explain threshold theorem, transversal gates, magic state distillation and lattice surgery at an overview level."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fault-tolerant gates and magic states
- Threshold theorem: arbitrary-length computation with polylog overhead if physical error is below threshold.
- Eastin-Knill: no code has a universal transversal gate set; use magic state injection plus distillation.
- Lattice surgery implements logical CNOT on surface codes.

## Gotchas
- T gates dominate resource estimates.

## Self-check
Estimate the T-factory overhead for a circuit with 10^6 T gates.
