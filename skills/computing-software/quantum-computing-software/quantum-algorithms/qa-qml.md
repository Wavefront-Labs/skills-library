---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-qml
name: qa-qml
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [quantum-machine-learning]
level: practitioner
status: draft
description: "Build feature-map kernels and variational classifiers and evaluate them against classical baselines."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quantum kernels and variational classifiers
```python
from sklearn.svm import SVC
# kernel matrix K_ij = |<phi(x_i)|phi(x_j)>|^2 computed with a fidelity circuit
clf = SVC(kernel="precomputed").fit(K_train, y)
```
- PennyLane: AngleEmbedding + StronglyEntanglingLayers + optimizer; scikit-compatible kernels in qiskit-machine-learning.
- Always compare with a tuned classical baseline.

## Gotchas
- Exponentially concentrated kernels on wide circuits give constant, useless Gram matrices.

## Self-check
Classify a toy dataset and report accuracy against an RBF SVM.
