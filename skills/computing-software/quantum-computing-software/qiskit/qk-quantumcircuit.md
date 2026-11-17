---
id: computing-software.quantum-computing-software.qiskit.qk-quantumcircuit
name: qk-quantumcircuit
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [quantumcircuit-basics, qiskit-circuits]
level: intro
status: draft
description: "Create circuits, add gates, registers and measurements, and inspect depth and operation counts."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QuantumCircuit construction and registers
```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
qc = QuantumCircuit(3, 3)          # 3 qubits, 3 classical bits
qc.h(0); qc.cx(0, 1); qc.cx(1, 2)
qc.measure([0, 1, 2], [0, 1, 2])   # or qc.measure_all()
print(qc.draw("text"), qc.depth(), qc.count_ops())
```
- Import path is qiskit; the pre-1.0 execute() function and qiskit.providers.aer import are removed (Qiskit 1.0+).
- measure_all() adds a fresh classical register named meas.

## Gotchas
- Bits in result strings are little-endian: classical bit 0 is rightmost.

## Self-check
Build a GHZ circuit and confirm count_ops shows 1 h, 2 cx, 3 measure.
