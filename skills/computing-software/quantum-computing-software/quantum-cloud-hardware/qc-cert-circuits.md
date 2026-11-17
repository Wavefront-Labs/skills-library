---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-cert-circuits
name: qc-cert-circuits
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [cert-circuit-operations, ibm-quantum-certification]
level: practitioner
status: draft
description: "Prepare for exam content on building circuits, gates and measurement with Qiskit (blueprint version unconfirmed)."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exam area: perform quantum operations
- IBM publishes a Qiskit developer exam (an associate-level exam, name and code depend on Qiskit major version, unconfirmed here); verify the current blueprint on the IBM training site.
- Typical areas: define circuits, apply gates, simulate and visualize results, run on hardware primitives, transpile.
```python
qc = QuantumCircuit(2,2); qc.h(0); qc.cx(0,1); qc.measure([0,1],[0,1])
```

## Gotchas
- Check the Qiskit version in the exam objectives: the 1.x to 2.x API changes matter.

## Self-check
Re-create each objective listed in the current blueprint with a runnable snippet.
