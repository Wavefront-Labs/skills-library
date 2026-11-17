---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-expect-pauli
name: qf-expect-pauli
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [expectation-values-pauli]
level: practitioner
status: draft
description: "Estimate expectation values of Pauli observables by basis change and group commuting terms."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Expectation values of Pauli strings
```python
from qiskit.quantum_info import SparsePauliOp, Statevector
H = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 0.5)])
Statevector(qc).expectation_value(H)
```
- On hardware use Estimator primitives; terms that commute qubit-wise can share one measurement setting.
- Variance shrinks as 1/shots.

## Gotchas
- Qiskit Pauli strings are little-endian: "XI" puts X on qubit 1.

## Self-check
Compare exact and 8192-shot estimates of <ZZ> on a Bell state.
