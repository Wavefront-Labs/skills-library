---
id: computing-software.quantum-computing-software.qiskit.qk-transpile-basics
name: qk-transpile-basics
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [transpile-optimization-level, qiskit-transpile]
level: practitioner
status: draft
description: "Transpile circuits to a backend target, choosing optimization level 0-3 and seeding for reproducibility."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# transpile and optimization levels
```python
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
pm = generate_preset_pass_manager(optimization_level=2, backend=backend, seed_transpiler=7)
isa = pm.run(qc)
```
- Level 0 maps only; 1 light; 2 medium; 3 heavy and slowest.
- Compare isa.depth() and isa.count_ops()["cx"/"ecr"/"cz"] across levels and seeds.

## Gotchas
- Layout and routing are stochastic; set a seed for comparable benchmarks.

## Self-check
Transpile a 5-qubit circuit at levels 0 and 3 and compare two-qubit gate counts.
