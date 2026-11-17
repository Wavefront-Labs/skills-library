---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-pl-measure
name: cp-pl-measure
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [pennylane-measurements]
level: practitioner
status: draft
description: "Choose expval, var, probs, sample, counts and state return types and observables."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measurement returns
- qml.expval(qml.PauliZ(0) @ qml.PauliZ(1)), qml.var, qml.probs(wires=[0,1]), qml.sample(), qml.counts(), qml.state().
- Hamiltonian terms: qml.Hamiltonian(coeffs, ops) or qml.dot / operator arithmetic.
```python
H = 0.5 * qml.PauliX(0) @ qml.PauliX(1) + qml.PauliZ(0)
```

## Gotchas
- state() requires analytic mode; Hamiltonians with non-commuting terms are measured by grouping.

## Self-check
Return probs for a Bell circuit and verify [0.5, 0, 0, 0.5].
