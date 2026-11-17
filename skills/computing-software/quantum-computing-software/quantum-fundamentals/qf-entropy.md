---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-entropy
name: qf-entropy
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [von-neumann-entropy]
level: advanced
status: draft
description: "Compute von Neumann entropy, mutual information and entanglement entropy of reduced states."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Von Neumann entropy and mutual information
```python
from qiskit.quantum_info import entropy, mutual_information
entropy(rho, base=2); mutual_information(rho_ab, base=2)
```
- S(rho) = -Tr rho log2 rho; pure states have S = 0; maximally mixed qubit S = 1.
- For pure bipartite states, entanglement entropy S(A) = S(B).

## Gotchas
- Mutual information of a Bell pair is 2 bits, counting quantum plus classical correlations.

## Self-check
Verify S is 1 bit for I/2.
