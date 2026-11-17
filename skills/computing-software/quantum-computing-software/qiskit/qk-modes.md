---
id: computing-software.quantum-computing-software.qiskit.qk-modes
name: qk-modes
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [runtime-execution-modes]
level: practitioner
status: draft
description: "Choose job, batch or session execution mode and understand queue and billing trade-offs."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Execution modes: job, session, batch
```python
from qiskit_ibm_runtime import Batch, Session, SamplerV2
with Batch(backend=backend) as b:
    sampler = SamplerV2(mode=b)
```
- Job: single primitive call; Batch: independent jobs, parallel; Session: dedicated access for iterative loops (availability depends on plan, unconfirmed).
- Open-plan limits on usage and modes change; read the plan docs.

## Gotchas
- Sessions that sit idle still use the time window.

## Self-check
Run a VQE-style loop in a session and a sweep in a batch.
