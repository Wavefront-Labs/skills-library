---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-cirq-qubits
name: cp-cirq-qubits
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [cirq-qubits-gates, cirq-circuits]
level: intro
status: draft
description: "Create LineQubit and GridQubit objects, append operations and print a Cirq circuit."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cirq qubits, gates and Circuit
```python
import cirq
q0, q1 = cirq.LineQubit.range(2)
c = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key="m"))
print(c)
```
- Gates are applied to qubits as cirq.X(q); Circuit holds Moments.
- Qubits order big-endian in results (first qubit most significant).

## Gotchas
- Measurement keys must be unique within a circuit unless repeated on purpose.

## Self-check
Print the circuit and confirm two moments before measurement.
