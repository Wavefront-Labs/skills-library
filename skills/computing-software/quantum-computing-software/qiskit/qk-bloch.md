---
id: computing-software.quantum-computing-software.qiskit.qk-bloch
name: qk-bloch
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [state-visualization]
level: intro
status: draft
description: "Plot states with Bloch spheres, city plots, Q-spheres and hinton plots."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# State visualizations
```python
from qiskit.visualization import plot_state_city, plot_bloch_multivector, plot_state_qsphere
```
- Works on Statevector and DensityMatrix objects.

## Gotchas
- Mixed or entangled states appear short or zero length on per-qubit Bloch vectors.

## Self-check
Plot a Bell state and note the zero-length vectors.
