---
id: computing-software.quantum-computing-software.qiskit.qk-target
name: qk-target
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [backend-target-isa]
level: practitioner
status: draft
description: "Read a backend's Target for operations, coupling and error rates, and understand ISA circuits."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Target, coupling map and basis gates
```python
t = backend.target
t.operation_names; backend.coupling_map
t["cx"] if "cx" in t else None
```
- Hardware jobs must be ISA circuits: only native gates on connected qubits.
- Target holds per-qubit properties such as gate error and duration.

## Gotchas
- Do not hard-code basis gates; they differ by device (ecr, cz, sx, rz, x are examples).

## Self-check
List two-qubit gate error for each edge and find the worst.
