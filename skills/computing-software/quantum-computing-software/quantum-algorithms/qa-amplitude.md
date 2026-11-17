---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-amplitude
name: qa-amplitude
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [amplitude-amplification]
level: advanced
status: draft
description: "Generalize Grover to amplitude amplification and estimate marked-item counts with quantum counting."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Amplitude amplification and counting
- Amplification works with any state-preparation A and reflection about good states: Q = -A S0 A^-1 S_good.
- Quantum counting runs phase estimation on Q to estimate theta and so M.
- Amplitude estimation variants (iterative, maximum-likelihood) avoid the QFT depth.
```python
from qiskit_algorithms import AmplitudeEstimation   # separate package, unconfirmed API per version
```

## Gotchas
- Mid-circuit-depth growth makes hardware estimation hard; check noise before trusting estimates.

## Self-check
Estimate the amplitude of a biased coin state with 3 evaluation qubits.
