---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-pl-ml
name: cp-pl-ml
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [pennylane-optimizers]
level: practitioner
status: draft
description: "Optimize QNode parameters with PennyLane optimizers and autograd, JAX, Torch interfaces."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interfaces and optimizers
```python
from pennylane import numpy as pnp
opt = qml.AdamOptimizer(stepsize=0.1)
params = pnp.array([0.1, 0.2], requires_grad=True)
for _ in range(50): params = opt.step(cost, params)
```
- Use requires_grad=True on trainable arrays from pennylane.numpy.
- Interfaces: autograd (default), jax, torch, tensorflow via qml.qnode(interface=...).

## Gotchas
- Plain numpy arrays are not trainable.

## Self-check
Minimize expval(Z) to -1 with RX.
