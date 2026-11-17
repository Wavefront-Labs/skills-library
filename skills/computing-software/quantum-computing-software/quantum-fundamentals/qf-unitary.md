---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-unitary
name: qf-unitary
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [unitary-composition, circuit-model]
level: practitioner
status: draft
description: "Compose circuits as matrix products and extract the unitary of a circuit."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unitary matrices and circuit composition
A circuit's unitary is the product of gate matrices, last gate leftmost.
```python
from qiskit.quantum_info import Operator
U = Operator(qc); assert U.is_unitary()
U2 = Operator(qc2).compose(U)      # apply qc first then qc2
```
- Inverse: qc.inverse(); the adjoint of a product reverses order.
- Equivalence up to global phase: Operator(a).equiv(Operator(b)).

## Gotchas
- Operator.compose(other) applies other first; use .dot for the opposite order.

## Self-check
Check U times U-dagger is the identity.
