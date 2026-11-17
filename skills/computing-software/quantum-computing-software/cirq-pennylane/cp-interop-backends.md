---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-interop-backends
name: cp-interop-backends
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [multi-backend-execution]
level: practitioner
status: draft
description: "Use PennyLane device plugins to run the same QNode on Aer, Cirq or cloud hardware by swapping the device string."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running one circuit on many backends
```python
dev = qml.device("qiskit.aer", wires=2)         # pennylane-qiskit plugin
dev = qml.device("cirq.simulator", wires=2)     # pennylane-cirq plugin
dev = qml.device("lightning.qubit", wires=2)    # pennylane-lightning
```
- Install the plugin package first; device names depend on plugin version (check docs).

## Gotchas
- Results differ by shots and noise; compare with shots=None where supported.

## Self-check
Run the same QNode on two devices and compare expectation values.
