---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-resource
name: qe-resource
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [resource-estimation-tools, resource-estimation]
level: sme
status: draft
description: "Run a resource estimator to turn algorithm logical counts into physical qubits and runtime under a hardware model."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resource estimation tooling
- Inputs: logical qubit count, T count, rotation count, depth; hardware profile (error rate, gate times); QEC scheme; error budget.
- Azure Quantum Resource Estimator and Qualtran provide this; check current docs for API.
```python
# qsharp.estimate(...) in the qsharp Python package; schema version-specific (unconfirmed)
```

## Gotchas
- Estimates are order-of-magnitude, not guarantees.

## Self-check
Compare estimates at error budgets 1e-3 and 1e-6.
