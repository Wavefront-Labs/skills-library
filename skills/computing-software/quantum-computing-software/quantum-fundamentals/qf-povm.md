---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-povm
name: qf-povm
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [povm]
level: advanced
status: draft
description: "Describe generalized measurements as POVMs and implement them with an ancilla and projective measurement."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# POVM and generalized measurement
POVM elements E_m are positive with sum E_m = I; P(m)=Tr(E_m rho). Naimark dilation realizes any POVM as a projective measurement on a larger space.
- Example: unambiguous discrimination of two non-orthogonal states, with an inconclusive outcome.
- Use mid-circuit measurement plus ancilla qubits for the dilation.

## Gotchas
- POVM elements need not be projectors or orthogonal, and there can be more outcomes than dimensions.

## Self-check
Verify the three-outcome trine POVM sums to identity.
