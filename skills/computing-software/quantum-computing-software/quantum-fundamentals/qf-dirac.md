---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-dirac
name: qf-dirac
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [dirac-notation, dirac-linear-algebra]
level: intro
status: draft
description: "Translate bra-ket expressions to vectors and matrices and compute inner and outer products in NumPy."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dirac notation, inner and outer products
- |psi> column vector, <psi| conjugate transpose, <a|b> inner product, |a><b| outer product (matrix).
```python
import numpy as np
a = np.array([1, 0]); b = np.array([1, 1]) / np.sqrt(2)
inner = np.vdot(a, b); outer = np.outer(a, b.conj())
```
- np.vdot conjugates the first argument; np.dot does not.

## Gotchas
- Using np.dot on complex vectors gives wrong inner products.

## Self-check
Check <+|-> = 0.
