---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-readout
name: qe-readout
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [readout-error-mitigation]
level: practitioner
status: draft
description: "Calibrate the assignment matrix and invert it or use M3-style methods to correct counts."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Readout error mitigation
```python
from mitiq.rem import generate_inverse_confusion_matrix
```
- Confusion matrix A_ij = P(measure i | prepared j); mitigated = A^-1 counts, with non-negativity fix.
- Tensored (per-qubit) assignment scales to many qubits; full matrix does not.

## Gotchas
- Inversion can produce negative probabilities; project back to the simplex.

## Self-check
Correct counts for |11> prepared with a 3 percent readout flip.
