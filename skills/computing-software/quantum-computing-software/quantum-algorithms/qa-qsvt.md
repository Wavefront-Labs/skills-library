---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-qsvt
name: qa-qsvt
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [qsvt-block-encoding]
level: sme
status: draft
description: "Name the block-encoding toolbox that gives optimal Hamiltonian simulation and its cost model."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Qubitization, LCU and QSVT
- Block encoding embeds a non-unitary matrix A as a sub-block of a unitary; LCU builds it from a sum of Paulis.
- QSVT applies a polynomial to singular values with a sequence of phase rotations; unifies simulation, matrix inversion and amplitude amplification.
- Simulation cost O(t + log(1/eps)) queries in the optimal form.
```python
# PennyLane: qml.qsvt / qml.BlockEncode; availability varies by version (unconfirmed)
```

## Gotchas
- Constant factors and ancilla counts are large; asymptotics do not imply practicality.

## Self-check
State the query cost of LCU-based simulation vs product formulas.
