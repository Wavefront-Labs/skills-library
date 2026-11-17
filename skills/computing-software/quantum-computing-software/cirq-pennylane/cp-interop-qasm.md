---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-interop-qasm
name: cp-interop-qasm
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [circuit-conversion-qasm, framework-interop]
level: practitioner
status: draft
description: "Move circuits among Qiskit, Cirq and PennyLane using OpenQASM and plugin converters."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Convert between frameworks via OpenQASM
```python
from qiskit import qasm2, qasm3
text = qasm2.dumps(qc)                      # Qiskit to OpenQASM 2
import cirq; c = cirq.contrib.qasm_import.circuit_from_qasm(text)
qml.from_qasm(text)                         # PennyLane
```
- Plugins also convert directly: qml.from_qiskit(qc), pennylane-qiskit, pennylane-cirq.
- Parameters and custom gates may not survive; verify unitary equality after conversion.

## Gotchas
- Bit ordering differs; check after the round trip.

## Self-check
Round-trip a Bell circuit and compare final state vectors.
