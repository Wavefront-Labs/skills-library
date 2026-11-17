---
id: computing-software.quantum-computing-software.qiskit.qk-passmanager
name: qk-passmanager
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [custom-passmanager]
level: advanced
status: draft
description: "Build staged pass managers and choose layout and routing methods such as SABRE."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom PassManager and layout/routing
```python
from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.passes import Optimize1qGatesDecomposition
pm = PassManager([Optimize1qGatesDecomposition(basis=["rz","sx","x"])])
```
- Stages: init, layout, routing, translation, optimization, scheduling.
- Provide initial_layout to pin logical-to-physical mapping to your best qubits.

## Gotchas
- Custom passes must preserve the target basis or the backend will reject the circuit.

## Self-check
Pin initial_layout to the lowest-error line of qubits and compare fidelity.
