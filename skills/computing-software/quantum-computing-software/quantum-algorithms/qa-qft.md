---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-qft
name: qa-qft
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [quantum-fourier-transform, qft-phase-estimation]
level: practitioner
status: draft
description: "Build the QFT from Hadamards, controlled phases and swaps, with O(n^2) gates and bit-reversal handling."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quantum Fourier transform circuit
QFT|j> = (1/sqrt N) sum_k e^(2 pi i jk/N)|k>.
```python
from qiskit.circuit.library import QFT
qc.compose(QFT(n, do_swaps=True), inplace=True)
qc.compose(QFT(n, inverse=True), inplace=True)
```
- Per qubit: H then controlled-phase rotations pi/2^k, then final swaps.
- Approximate QFT drops tiny rotations to cut depth.

## Gotchas
- Forgetting swaps reverses the output bit order.

## Self-check
Apply QFT then inverse QFT and get the identity.
