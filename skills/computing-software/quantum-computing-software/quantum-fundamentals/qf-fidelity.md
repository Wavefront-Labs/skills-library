---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-fidelity
name: qf-fidelity
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [fidelity-trace-distance, quantum-information-measures]
level: advanced
status: draft
description: "Compare states with fidelity and trace distance and know the Fuchs-van de Graaf relation."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fidelity and trace distance
```python
from qiskit.quantum_info import state_fidelity, DensityMatrix
state_fidelity(rho, sigma)       # squared-overlap convention in Qiskit
```
- Fidelity conventions differ (F vs sqrt F); check the library docs.
- Trace distance D = 0.5 ||rho - sigma||_1; bounds 1 - sqrt(F) <= D <= sqrt(1 - F) with F the squared form.

## Gotchas
- Quote the convention when reporting fidelities.

## Self-check
Compute D and F for |0> and |+>.
