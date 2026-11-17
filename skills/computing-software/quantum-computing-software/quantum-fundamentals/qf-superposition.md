---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-superposition
name: qf-superposition
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [superposition-amplitudes]
level: intro
status: draft
description: "Write normalized superpositions, read amplitudes and probabilities, and tell global from relative phase."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Superposition and amplitudes
A qubit state is a|0>+b|1> with |a|^2+|b|^2=1; amplitudes are complex, probabilities are squared magnitudes.
```python
import numpy as np
psi = np.array([1, 1j]) / np.sqrt(2)
assert np.isclose(np.vdot(psi, psi).real, 1)
probs = np.abs(psi) ** 2          # [0.5, 0.5]
```
- Global phase e^(i g)|psi> is unobservable; relative phase between amplitudes changes interference and X/Y-basis outcomes.
- |+> and |-> have identical Z-measurement statistics but differ in phase.

## Gotchas
- Forgetting normalization when building states by hand gives probabilities that do not sum to 1.

## Self-check
Show (|0>+|1>)/sqrt2 and (|0>+i|1>)/sqrt2 give the same Z statistics but different Y outcomes.
