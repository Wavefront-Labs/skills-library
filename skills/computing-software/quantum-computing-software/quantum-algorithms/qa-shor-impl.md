---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-shor-impl
name: qa-shor-impl
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [shor-implementation]
level: sme
status: draft
description: "Understand resource scaling of Shor's algorithm and why textbook demos factor only tiny numbers."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Implementing Shor with modular arithmetic
- Needs about 2n+3 qubits in simple designs; Gidney-Ekera style estimates are on the order of millions of noisy qubits for RSA-2048 (figures from the literature, unconfirmed here).
- Toy circuits for N=15 are often hand-simplified using known a; this is not general factoring.
- Defensive relevance: justifies post-quantum migration timelines (see NIST PQC skills).

## Gotchas
- Demo circuits with precomputed modular exponentiation prove nothing about scalability.

## Self-check
List the gates in a controlled-modular-multiplier for N=15.
