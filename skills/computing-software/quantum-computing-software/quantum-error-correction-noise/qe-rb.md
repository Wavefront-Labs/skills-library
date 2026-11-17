---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-rb
name: qe-rb
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [randomized-benchmarking, device-benchmarking]
level: advanced
status: draft
description: "Measure average gate fidelity from random Clifford sequences by fitting exponential decay."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Randomized benchmarking
```python
from qiskit_experiments.library import StandardRB
exp = StandardRB(physical_qubits=(0,), lengths=[1,10,50,100,200], num_samples=10)
```
- Fit A p^m + B; error per Clifford r = (1-p)(d-1)/d with d=2^n.
- Interleaved RB isolates a single gate.

## Gotchas
- RB is SPAM-robust but not a complete characterization; coherent error is under-reported.

## Self-check
Fit a decay and report error per Clifford.
