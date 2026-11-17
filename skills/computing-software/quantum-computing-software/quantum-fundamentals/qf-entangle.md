---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-entangle
name: qf-entangle
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [entanglement-bell-states]
level: intro
status: draft
description: "Create the four Bell states, show non-separability and verify correlations in code."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entanglement and Bell states
Bell state |Phi+> = (|00>+|11>)/sqrt2 is not a product of single-qubit states.
```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2); qc.h(0); qc.cx(0, 1)      # |Phi+>
# other Bell states: add x(0) / z(0) before h, or x(1) after cx
```
- Test separability of a pure 2-qubit state: reduced state of one qubit has purity < 1 iff entangled.
- Bell inequality (CHSH) maximum for quantum is 2*sqrt2 against classical bound 2.

## Gotchas
- Marginal measurement counts of a Bell pair look random; correlation shows only when both qubits are compared.

## Self-check
Measure both qubits of |Phi+> and confirm only 00 and 11 occur.
