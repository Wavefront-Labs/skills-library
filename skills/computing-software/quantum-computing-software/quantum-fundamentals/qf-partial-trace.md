---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-partial-trace
name: qf-partial-trace
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [partial-trace-reduced-state]
level: practitioner
status: draft
description: "Trace out subsystems to get reduced density matrices and measure entanglement via purity or entropy."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Partial trace and reduced states
```python
from qiskit.quantum_info import Statevector, partial_trace, entropy
rho = partial_trace(Statevector(bell_circuit), [1])
print(rho.purity(), entropy(rho, base=2))   # Bell: purity 0.5, entropy 1 bit
```
- Reduced state of a maximally entangled pair is maximally mixed (I/2).
- Entanglement entropy S = -Tr(rho log rho) equals 0 for product pure states.

## Gotchas
- Qiskit partial_trace takes the list of qubits to trace OUT, not to keep.

## Self-check
Verify trace of rho is 1 and purity of a product state is 1.
