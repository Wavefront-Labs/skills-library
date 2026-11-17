---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-controlled
name: qf-controlled
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [controlled-gates-cnot]
level: intro
status: draft
description: "Use CNOT, CZ, SWAP and Toffoli and understand control/target roles, including phase kickback."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Controlled gates and CNOT
```python
qc.cx(c, t); qc.cz(a, b); qc.swap(a, b); qc.ccx(c1, c2, t)
```
- CNOT flips target if control is |1>; CZ is symmetric; CNOT = (I x H) CZ (I x H).
- Phase kickback: a control in superposition picks up the target eigenvalue phase, the engine behind phase estimation.
- SWAP = three CNOTs.

## Gotchas
- CNOT on a control in superposition entangles; it is not a classical copy (no-cloning).

## Self-check
Build a Toffoli truth table with ccx on all 8 inputs.
