---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-qrng
name: qa-qrng
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [quantum-random-numbers]
level: intro
status: draft
description: "Generate random bits with H and measurement and understand why simulators are only pseudorandom."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quantum random number generation
```python
qc = QuantumCircuit(8); qc.h(range(8)); qc.measure_all()
```
- Simulators use a PRNG; real hardware has bias and correlations, so apply randomness extraction before cryptographic use.
- Hardware readout bias often exceeds 1%.

## Gotchas
- Never use raw device output as key material without testing and extraction.

## Self-check
Run NIST randomness tests (SP 800-22) on 1 Mbit of output.
