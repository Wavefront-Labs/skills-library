---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-bloch-sphere
name: qf-bloch-sphere
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [bloch-sphere, qubit-state]
level: intro
status: draft
description: "Map a single-qubit state to Bloch sphere angles theta and phi and read poles, equator and phase."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bloch sphere representation
State |psi> = cos(theta/2)|0> + e^(i phi) sin(theta/2)|1>, with 0<=theta<=pi, 0<=phi<2pi.
- |0> north pole, |1> south pole, |+> and |-> on the x axis, |+i> and |-i> on the y axis.
- Bloch vector = (<X>,<Y>,<Z>); pure states lie on the surface, mixed states inside.
```python
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
plot_bloch_multivector(Statevector.from_label("+"))
```

## Gotchas
- Global phase is invisible on the sphere; relative phase phi is the longitude.
- Orthogonal states are antipodal (angle pi on the sphere), not 90 degrees apart.

## Self-check
Compute (<X>,<Y>,<Z>) for |+i> and confirm it is (0,1,0).
