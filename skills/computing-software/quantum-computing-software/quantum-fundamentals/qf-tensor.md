---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-tensor
name: qf-tensor
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [tensor-products, multi-qubit-systems]
level: practitioner
status: draft
description: "Build multi-qubit states and operators with Kronecker products and get the endianness convention right."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tensor products and qubit ordering
n qubits span a 2^n dimensional space; operators combine with the Kronecker product.
```python
import numpy as np
X=np.array([[0,1],[1,0]]); I=np.eye(2)
np.kron(X, I)          # textbook: X on the FIRST (leftmost) qubit
```
- Qiskit labels are little-endian: in "q2 q1 q0" strings qubit 0 is rightmost, so Qiskit's matrix for X on qubit 0 is np.kron(I, X).
- Cirq and PennyLane print qubit 0 first (big-endian wire order).

## Gotchas
- Mixing conventions silently transposes your circuit; convert before comparing across frameworks.

## Self-check
Prepare |10> in Qiskit (x on qubit 1) and confirm the statevector label is "10" with index 2.
