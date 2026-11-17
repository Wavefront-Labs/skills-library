---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-universal
name: qf-universal
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [universal-gate-sets]
level: advanced
status: draft
description: "State which gate sets are universal, the Solovay-Kitaev result and the Clifford+T decomposition cost."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Universal gate sets
- Universal approximately: {H, T, CNOT} (Clifford+T), or arbitrary single-qubit gates plus CNOT (exactly universal).
- Solovay-Kitaev: approximate any gate to error eps with polylog(1/eps) gates (exponent about 3.97 in the basic form).
- Clifford alone is not universal (Gottesman-Knill: classically simulable).
```python
from qiskit import transpile
transpile(qc, basis_gates=["h","t","tdg","cx"], optimization_level=1)
```

## Gotchas
- T count dominates fault-tolerant cost; minimize it, not total depth.

## Self-check
Decompose an Rz(0.1) into Clifford+T with transpile and count T gates.
