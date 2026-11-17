---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-zne
name: qe-zne
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [zero-noise-extrapolation, error-mitigation]
level: advanced
status: draft
description: "Amplify noise by gate folding, measure at several scale factors and extrapolate to zero noise."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zero-noise extrapolation
```python
from mitiq import zne
mitigated = zne.execute_with_zne(circuit, executor)   # executor returns expectation value
```
- Scale factors typically 1, 3, 5 by unitary folding G -> G G^dagger G; Richardson, linear or exponential fit.
- Qiskit Runtime offers ZNE as a resilience option (check the version).

## Gotchas
- Extrapolation increases variance and can overshoot; report error bars.

## Self-check
Mitigate a depth-20 circuit under a depolarizing model and show the improvement.
