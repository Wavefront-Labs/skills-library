---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-ibm-platform
name: qc-ibm-platform
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [ibm-quantum-backends]
level: practitioner
status: draft
description: "Choose a backend by qubits, error rate and queue, and check status and calibration."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IBM Quantum Platform backends and queue
```python
service.backends(min_num_qubits=100, operational=True)
b = service.backend("<backend_name>"); b.status().pending_jobs
```
- Prefer low two-qubit error and short queues; calibration refreshes at least daily.

## Gotchas
- Backend names change as devices retire; avoid hard-coding.

## Self-check
Pick the best backend by 2q error among five candidates.
