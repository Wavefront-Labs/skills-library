---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-kraus
name: qf-kraus
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [quantum-channels-kraus]
level: advanced
status: draft
description: "Represent noise and operations as CPTP maps with Kraus operators and check completeness."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quantum channels and Kraus operators
E(rho)=sum_k K_k rho K_k^dagger with sum K_k^dagger K_k = I.
```python
from qiskit.quantum_info import Kraus
import numpy as np
p=0.1
K = Kraus([np.sqrt(1-p)*np.eye(2), np.sqrt(p)*np.array([[0,1],[1,0]])])   # bit-flip
K.is_cptp()
```
- Equivalent forms: Choi matrix, superoperator, Stinespring dilation.

## Gotchas
- Kraus decomposition is not unique; compare channels via Choi, not Kraus lists.

## Self-check
Apply the channel to |0><0| and verify the output diag is [1-p, p].
