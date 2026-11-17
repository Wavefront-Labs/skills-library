---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-nocloning
name: qf-nocloning
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [no-cloning-teleportation]
level: practitioner
status: draft
description: "Explain the no-cloning theorem and implement quantum teleportation with classical correction."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# No-cloning and teleportation
No unitary copies an unknown state. Teleportation moves |psi> using a Bell pair plus two classical bits.
```python
# q0 = psi, q1-q2 Bell pair; Alice: cx(0,1), h(0), measure q0,q1
# Bob: x on q2 if c1, z on q2 if c0 (dynamic circuit)
with qc.if_test((c1, 1)): qc.x(2)
with qc.if_test((c0, 1)): qc.z(2)
```
- Superdense coding is the dual: one qubit carries two classical bits using a shared Bell pair.

## Gotchas
- Corrections are conditional on measurement results; skipping them leaves a random Pauli error.

## Self-check
Teleport |+i> and verify Bob's Bloch vector matches.
