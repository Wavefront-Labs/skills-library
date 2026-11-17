---
id: computing-software.quantum-computing-software.qiskit.qk-account
name: qk-account
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [ibm-quantum-account, qiskit-runtime]
level: practitioner
status: draft
description: "Save an IBM Quantum Platform credential and instantiate QiskitRuntimeService safely."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Account setup and authentication
```python
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token="<API_KEY>", instance="<CRN>", overwrite=True)
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=5)
```
- Channel names have changed over time (ibm_quantum, ibm_cloud, ibm_quantum_platform); check the docs for your version, unconfirmed.
- Credentials are stored in a local file in your home directory; never commit tokens.

## Gotchas
- Store the key in a secret manager or env var in CI.

## Self-check
List backends and print status of the least busy one.
