---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-pl-templates-layers
name: cp-pl-templates-layers
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [pennylane-templates-layers, pennylane-templates]
level: practitioner
status: draft
description: "Use templates such as StronglyEntanglingLayers and AngleEmbedding to build variational circuits."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Templates and embeddings
```python
shape = qml.StronglyEntanglingLayers.shape(n_layers=3, n_wires=4)
weights = pnp.random.random(shape, requires_grad=True)
qml.StronglyEntanglingLayers(weights, wires=range(4))
qml.AngleEmbedding(x, wires=range(4))
```
- Others: BasicEntanglerLayers, AmplitudeEmbedding, IQPEmbedding.

## Gotchas
- Weight tensor shape depends on the template; use its .shape helper.

## Self-check
Count trainable parameters for 3 layers on 4 wires (36).
