---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-native
name: qc-native
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [native-gates-connectivity]
level: practitioner
status: draft
description: "Read a backend's native gates and coupling and design circuits that minimize routing cost."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Native gates and connectivity constraints
- Example native sets: rz, sx, x with ecr/cz/cx; ions use MS or ZZ; neutral atoms use CZ via Rydberg.
- Each SWAP costs 3 two-qubit gates; choose layouts to fit the problem graph.
```python
backend.target.operation_names; backend.coupling_map.get_edges()
```

## Gotchas
- Do not assume cx is native; the transpiler synthesises it.

## Self-check
List native two-qubit gate and edge count for a backend.
