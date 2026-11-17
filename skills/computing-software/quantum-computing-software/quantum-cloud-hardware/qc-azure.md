---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-azure
name: qc-azure
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [azure-quantum]
level: practitioner
status: draft
description: "Submit jobs to Azure Quantum providers using the Python SDK and Q# or QIR programs."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Azure Quantum and Q#
```python
from azure.quantum import Workspace
ws = Workspace(resource_id="<resource-id>", location="<region>")
```
- Providers expose targets; QIR (LLVM-based) is the common program format.
- Resource Estimator is available as a target (see resource estimation skill).

## Gotchas
- Provider catalog and Q# tooling changed repeatedly; check current docs, unconfirmed.

## Self-check
List targets for your workspace.
