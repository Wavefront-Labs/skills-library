---
id: computing-software.quantum-computing-software.qiskit.qk-opflow
name: qk-opflow
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [qiskit-algorithms-migration]
level: advanced
status: draft
description: "Migrate from removed opflow and qiskit.algorithms to SparsePauliOp and the separate qiskit-algorithms package."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Operators and the Qiskit Algorithms migration
- qiskit.opflow and qiskit.utils.QuantumInstance were removed (Qiskit 1.0); use SparsePauliOp and primitives.
- Algorithms (VQE, QAOA, Grover) live in the separate qiskit-algorithms package, community-maintained; import from qiskit_algorithms.
```python
# pip install qiskit-algorithms
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
```
- qiskit-nature, qiskit-optimization and qiskit-machine-learning are separate packages with their own versions.

## Gotchas
- Old tutorials with execute(), Aer.get_backend or opflow will not run on current Qiskit.

## Self-check
Port a code snippet using execute() to SamplerV2.
