---
id: computing-software.quantum-computing-software.qiskit.qk-control-flow
name: qk-control-flow
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [dynamic-circuits]
level: advanced
status: draft
description: "Use if_test, while_loop, for_loop and switch with mid-circuit measurement for dynamic circuits."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic circuits and control flow
```python
with qc.if_test((qc.clbits[0], 1)):
    qc.x(1)
with qc.for_loop(range(3)):
    qc.h(0)
```
- Backend must support the control-flow instructions (check target.operation_names).
- Mid-circuit measurement and reset take longer than gates; check the backend for latency and conditional-gate support.

## Gotchas
- Classical registers used in conditions must exist before the block.

## Self-check
Teleportation with if_test passes on a simulator.
