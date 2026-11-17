---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-qpe
name: qa-qpe
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [quantum-phase-estimation]
level: advanced
status: draft
description: "Estimate eigenphases of a unitary with t counting qubits, controlled powers and inverse QFT."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quantum phase estimation
```python
from qiskit.circuit.library import PhaseEstimation, QFT   # or build with cp and QFT inverse
# counting qubits in |+>, controlled-U^(2^j), inverse QFT, measure
```
- t qubits give about t bits of phase; precision with success prob 1-delta needs t = n + ceil(log2(2 + 1/(2 delta))).
- Eigenstate input is required; a superposition returns a superposition of phases.

## Gotchas
- U^(2^j) must be implemented efficiently, not by repeating U 2^j times in a deep circuit.

## Self-check
Estimate the phase of a T gate on |1> (phase 1/8) with 3 qubits.
