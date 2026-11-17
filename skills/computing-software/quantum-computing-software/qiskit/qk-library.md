---
id: computing-software.quantum-computing-software.qiskit.qk-library
name: qk-library
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [circuit-library-blocks, qiskit-circuit-library]
level: practitioner
status: draft
description: "Use library circuits such as QFT, EfficientSU2, TwoLocal and GroverOperator, plus operator-based gates."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Circuit library blocks
```python
from qiskit.circuit.library import QFT, EfficientSU2, TwoLocal
ansatz = EfficientSU2(4, reps=2, entanglement="linear")
qft = QFT(4, do_swaps=True)
```
- Newer releases prefer function forms (qft, efficient_su2) over class forms for some blocks (check version, unconfirmed).
- Use .decompose() or transpile to see native gates.

## Gotchas
- Class-based blocks are not auto-expanded; transpile before hardware.

## Self-check
Count parameters of EfficientSU2(4, reps=2).
