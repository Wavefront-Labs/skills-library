---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-qasm-qiskit
name: qc-qasm-qiskit
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [qasm3-qiskit-export]
level: practitioner
status: draft
description: "Round-trip circuits through Qiskit qasm3 dumps and loads and note unsupported features."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Import and export with Qiskit
```python
from qiskit import qasm3
text = qasm3.dumps(qc)
qc2 = qasm3.loads(text)            # needs qiskit_qasm3_import package
```
- Importing requires the optional qiskit-qasm3-import package (unconfirmed for latest release).

## Gotchas
- Round trip may rename registers and expand gates.

## Self-check
Check Operator(qc) equals Operator(qc2).
