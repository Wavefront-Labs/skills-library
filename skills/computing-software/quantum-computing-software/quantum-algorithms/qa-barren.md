---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-barren
name: qa-barren
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [barren-plateaus]
level: sme
status: draft
description: "Diagnose vanishing gradients in deep random variational circuits and apply structured ansatz or local costs."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Barren plateaus and trainability
- For random deep circuits gradient variance decays exponentially with qubit count (McClean et al. 2018).
- Mitigate with local cost functions, shallow structured ansatz, layerwise training, smart initialization.
```python
# measure Var of dC/dtheta across random seeds as n grows
```

## Gotchas
- Hardware noise can induce plateaus even for shallow circuits.

## Self-check
Plot gradient variance vs qubit count for a random ansatz.
