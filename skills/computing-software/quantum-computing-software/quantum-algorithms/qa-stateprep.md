---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-stateprep
name: qa-stateprep
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [amplitude-encoding, state-preparation]
level: advanced
status: draft
description: "Load classical vectors as amplitudes with exponential depth and compare with basis, angle encodings."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# State preparation and amplitude encoding
```python
from qiskit.circuit.library import StatePreparation
qc.append(StatePreparation(vec / np.linalg.norm(vec)), range(n))
qml.AmplitudeEmbedding(x, wires=range(n), normalize=True)
```
- Arbitrary 2^n amplitude states need about 2^n gates; special structure (sparse, Gaussian) is cheaper.

## Gotchas
- Normalize first; encoding cost often cancels the claimed speedup.

## Self-check
Prepare [0.5,0.5,0.5,0.5] and confirm via Statevector.
