---
id: computing-software.quantum-computing-software.qiskit.qk-aer
name: qk-aer
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [aer-simulator, qiskit-simulation]
level: practitioner
status: draft
description: "Run fast simulations with AerSimulator methods and noise models, via the separate qiskit-aer package."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Qiskit Aer simulators
```python
# pip install qiskit-aer
from qiskit_aer import AerSimulator
sim = AerSimulator(method="statevector")   # also stabilizer, density_matrix, matrix_product_state
```
- Stabilizer method scales to hundreds of qubits for Clifford-only circuits.
- AerSimulator.from_backend(backend) copies noise and coupling.

## Gotchas
- Statevector memory is 16 bytes times 2^n; about 30 qubits is about 16 GB.

## Self-check
Run a 40-qubit GHZ with the stabilizer method.
