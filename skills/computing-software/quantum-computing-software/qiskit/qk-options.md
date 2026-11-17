---
id: computing-software.quantum-computing-software.qiskit.qk-options
name: qk-options
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [runtime-options-resilience]
level: advanced
status: draft
description: "Set shots, dynamical decoupling, twirling and resilience options on Runtime primitives."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Runtime options and resilience
```python
est = EstimatorV2(mode=backend)
est.options.resilience_level = 1
est.options.dynamical_decoupling.enable = True
est.options.twirling.enable_gates = True
```
- Options differ by primitive and release; resilience_level semantics are version dependent (unconfirmed).

## Gotchas
- More mitigation multiplies shot overhead and runtime.

## Self-check
Compare level 0 and 1 expectation values against exact on a small circuit.
