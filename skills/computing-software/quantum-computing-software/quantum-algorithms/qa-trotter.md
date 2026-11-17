---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-trotter
name: qa-trotter
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [trotterization, hamiltonian-simulation]
level: advanced
status: draft
description: "Simulate e^(-iHt) with first- and second-order Trotter splitting and estimate step counts."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trotter-Suzuki product formulas
e^(-i(A+B)t) approx (e^(-iA t/r) e^(-iB t/r))^r, error O(t^2/r) first order, O(t^3/r^2) second order.
```python
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter
gate = PauliEvolutionGate(H, time=1.0, synthesis=SuzukiTrotter(order=2, reps=10))
```
- Group commuting terms to cut depth.

## Gotchas
- Error scales with commutators; non-commuting terms need more steps.

## Self-check
Compare Trotter output with exact matrix exponential on 3 qubits.
