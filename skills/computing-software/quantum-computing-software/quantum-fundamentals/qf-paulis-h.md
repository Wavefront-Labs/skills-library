---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-paulis-h
name: qf-paulis-h
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [single-qubit-gates, quantum-gates]
level: intro
status: draft
description: "Know the matrices and actions of X, Y, Z, H, S and T and their algebraic relations."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pauli, Hadamard, phase and T gates
- X bit flip, Z phase flip (Z|1>=-|1>), Y = iXZ; H swaps Z and X bases; S = sqrt(Z); T = sqrt(S) (pi/8 gate).
- Relations: HZH = X, HXH = Z, S^2 = Z, T^4 = Z, each Pauli squares to I, XY = iZ.
```python
qc.h(0); qc.s(0); qc.t(0); qc.sdg(0); qc.tdg(0)
```
- Clifford group (H, S, CNOT) maps Paulis to Paulis and is classically simulable; T adds universality.

## Gotchas
- Y has imaginary entries; mis-typing it as X-Z in code drops the factor i.

## Self-check
Multiply the matrices to confirm HZH equals X.
