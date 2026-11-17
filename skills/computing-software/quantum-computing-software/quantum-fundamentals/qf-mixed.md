---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-mixed
name: qf-mixed
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [mixed-states-purity, density-matrices]
level: practitioner
status: draft
description: "Use density matrices for ensembles, compute purity and distinguish pure from mixed states."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mixed states and purity
rho = sum_i p_i |psi_i><psi_i|; Tr(rho)=1, rho>=0; purity Tr(rho^2) in [1/d, 1].
```python
from qiskit.quantum_info import DensityMatrix
rho = DensityMatrix.from_label("0").evolve(qc)
rho.purity(); rho.is_valid()
```
- Different ensembles can give the same rho (no physical way to tell them apart).

## Gotchas
- A 50/50 classical mix of |0>,|1> is I/2 and differs from |+>, whose rho has off-diagonals.

## Self-check
Compute purity of I/2 and get 0.5.
