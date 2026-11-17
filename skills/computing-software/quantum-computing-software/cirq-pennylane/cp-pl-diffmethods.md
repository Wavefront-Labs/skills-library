---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-pl-diffmethods
name: cp-pl-diffmethods
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [pennylane-diff-method, pennylane-gradients]
level: practitioner
status: draft
description: "Select backprop, adjoint, parameter-shift or finite-diff for a QNode and know each one's constraints."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# diff_method choices
```python
@qml.qnode(dev, diff_method="parameter-shift")
```
- backprop: simulators only, fast, memory heavy; adjoint: statevector simulators; parameter-shift: works on hardware, 2 circuit evaluations per parameter per shifted gate.
- best (default) picks automatically.

## Gotchas
- With shots on a simulator, adjoint and backprop do not apply.

## Self-check
Compare gradients from all supported methods on a 3-parameter circuit.
