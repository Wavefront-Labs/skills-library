---
id: computing-software.quantum-computing-software.qiskit.qk-qinfo
name: qk-qinfo
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [quantum-info-module]
level: practitioner
status: draft
description: "Use qiskit.quantum_info for exact states, operators, SparsePauliOp and fidelity checks."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Statevector, Operator and Pauli algebra
```python
from qiskit.quantum_info import Statevector, Operator, SparsePauliOp, state_fidelity
state_fidelity(Statevector(a), Statevector(b))
SparsePauliOp.from_list([("XX",1),("ZI",.5)]).to_matrix(sparse=True)
```
- Use for unit tests: compare Operator(circuit) to a target matrix up to phase.

## Gotchas
- Dense matrices explode past about 14 qubits; use sparse or Aer.

## Self-check
Test that your decomposition equals its target with Operator.equiv.
