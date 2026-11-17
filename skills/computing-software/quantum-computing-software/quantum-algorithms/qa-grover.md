---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-grover
name: qa-grover
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [grovers-algorithm, grover-search]
level: practitioner
status: draft
description: "Build a Grover oracle and diffuser and pick the number of iterations near pi/4 sqrt(N/M)."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Grover's algorithm circuit
```python
import math
k = math.floor(math.pi / 4 * math.sqrt(N / M))
# per iteration: oracle (phase flip marked) then diffuser (H, X, multi-controlled Z, X, H)
from qiskit.circuit.library import grover_operator   # or GroverOperator in older releases
```
- Success probability sin^2((2k+1) theta) with sin(theta)=sqrt(M/N); overshooting lowers it.
- Quadratic speedup, optimal for unstructured search.

## Gotchas
- Unknown M needs the exponential-search or counting variant.

## Self-check
Mark |101> on 3 qubits and reach near 94.5% in 2 iterations.
