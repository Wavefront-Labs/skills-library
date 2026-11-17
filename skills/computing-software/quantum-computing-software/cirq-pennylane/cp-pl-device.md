---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-pl-device
name: cp-pl-device
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [pennylane-qnode-device, pennylane-qnode]
level: intro
status: draft
description: "Define a PennyLane QNode on a device such as default.qubit and call it like a function."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Devices and the QNode decorator
```python
import pennylane as qml
dev = qml.device("default.qubit", wires=2)
@qml.qnode(dev)
def circuit(x):
    qml.RX(x, wires=0); qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(1))
print(circuit(0.5)); print(qml.draw(circuit)(0.5))
```
- shots=None gives analytic results; pass shots=1000 for sampling.
- Plugins: lightning.qubit (fast C++), qiskit.aer, braket, cirq devices.

## Gotchas
- Wire order is big-endian in drawings and probabilities (wire 0 first).

## Self-check
Compare analytic and 1000-shot values.
