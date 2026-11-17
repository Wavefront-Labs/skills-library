---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-tomography
name: qe-tomography
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [quantum-tomography]
level: advanced
status: draft
description: "Reconstruct states or processes from measurements with linear inversion or maximum likelihood."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# State and process tomography
```python
from qiskit_experiments.library import StateTomography
```
- n-qubit full tomography needs about 3^n bases and 4^n parameters; infeasible beyond a few qubits.
- Shadow tomography and Pauli-estimation avoid full reconstruction.

## Gotchas
- Linear inversion yields unphysical states; use constrained MLE.

## Self-check
Tomograph a Bell state and compute fidelity.
