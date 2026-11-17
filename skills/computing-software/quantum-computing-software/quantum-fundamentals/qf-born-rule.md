---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-born-rule
name: qf-born-rule
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [measurement-born-rule]
level: intro
status: draft
description: "Apply the Born rule to compute outcome probabilities and post-measurement states in the computational basis."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measurement and the Born rule
P(k)=|<k|psi>|^2; after measuring k the state collapses to |k>.
```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
qc = QuantumCircuit(1); qc.h(0)
print(Statevector(qc).probabilities_dict())   # {'0': 0.5, '1': 0.5}
```
- Repeated measurement on the same collapsed state returns the same result.
- Sampling gives shot noise of order 1/sqrt(shots) on estimated probabilities.

## Gotchas
- Statevector probabilities are exact; sampler counts are statistical, so compare with tolerance.

## Self-check
Sample 4096 shots of H|0> and check each count is within a few percent of 2048.
