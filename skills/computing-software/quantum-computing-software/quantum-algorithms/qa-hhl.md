---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-hhl
name: qa-hhl
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [hhl, quantum-ml-linear]
level: sme
status: draft
description: "Describe HHL, its assumptions (sparse, well-conditioned, state output) and why speedups are caveated."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HHL linear systems algorithm
- Solves Ax=b to produce |x> in O(log N poly(kappa, s)) time, but needs state loading (qRAM) and only gives expectation-type readout.
- Dequantization results (Tang) show classical speedups for related ML tasks.
```python
# small demo with a 2x2 matrix in Qiskit using QPE + controlled rotations
```

## Gotchas
- Reading all entries of x costs O(N) and removes the speedup.

## Self-check
Run a 2x2 HHL demo and compare with numpy.linalg.solve.
