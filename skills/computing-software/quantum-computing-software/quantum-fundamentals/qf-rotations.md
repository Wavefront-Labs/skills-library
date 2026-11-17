---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-rotations
name: qf-rotations
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [rotation-gates]
level: practitioner
status: draft
description: "Use axis rotations Rx, Ry, Rz and the general U gate to prepare arbitrary single-qubit states."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rotation gates Rx Ry Rz
R_n(theta) = exp(-i theta n.sigma / 2); rotations by theta move the Bloch vector theta radians about the axis.
```python
qc.rx(theta, 0); qc.ry(theta, 0); qc.rz(phi, 0)
qc.u(theta, phi, lam, 0)     # U(theta,phi,lambda), any single-qubit unitary up to global phase
```
- Rz(phi) differs from the phase gate P(phi) only by global phase; hardware often implements Rz virtually (frame change).
- Any 1-qubit unitary = Rz Ry Rz (Euler decomposition).

## Gotchas
- Angles are radians and the half-angle convention means rx(pi) equals X up to phase -i.

## Self-check
Check ry(pi/2) on |0> gives |+> up to numerical tolerance.
