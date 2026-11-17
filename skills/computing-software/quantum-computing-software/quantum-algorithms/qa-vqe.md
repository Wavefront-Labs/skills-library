---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-vqe
name: qa-vqe
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [vqe, variational-algorithms]
level: practitioner
status: draft
description: "Run VQE with an ansatz, a SparsePauliOp Hamiltonian, an estimator and a classical optimizer."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VQE for ground-state energies
```python
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
vqe = VQE(estimator, ansatz, SLSQP())
result = vqe.compute_minimum_eigenvalue(H)
```
- Cost: E(theta) = <psi(theta)|H|psi(theta)>; variational principle bounds the true ground energy from above (noise-free).
- Choice of ansatz (hardware-efficient vs chemically inspired) drives expressibility and barren plateaus.

## Gotchas
- Noisy hardware can return energies below the true minimum due to measurement noise; do not trust sub-ground values.

## Self-check
Reproduce H2 energy on a simulator.
