---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-qaoa
name: qa-qaoa
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [qaoa]
level: practitioner
status: draft
description: "Encode MaxCut as an Ising Hamiltonian and run QAOA with p layers and classical optimization."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QAOA for combinatorial optimization
- Cost layer exp(-i gamma C), mixer exp(-i beta sum X); p layers have 2p parameters.
- MaxCut: C = sum over edges (1 - Z_i Z_j)/2.
```python
from qiskit.circuit.library import QAOAAnsatz
ansatz = QAOAAnsatz(cost_operator=H, reps=2)
```
- Performance depends on p; compare against classical heuristics (Goemans-Williamson).

## Gotchas
- Quantum advantage is not established for QAOA at low depth.

## Self-check
Solve a 4-node cycle MaxCut and compare with brute force.
