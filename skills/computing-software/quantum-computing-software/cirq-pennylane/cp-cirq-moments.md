---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-cirq-moments
name: cp-cirq-moments
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [cirq-moments-insert]
level: practitioner
status: draft
description: "Control scheduling with Moment objects and InsertStrategy EARLIEST, NEW, INLINE."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Moments and InsertStrategy
```python
c = cirq.Circuit()
c.append([cirq.X(q0), cirq.Y(q1)], strategy=cirq.InsertStrategy.EARLIEST)
c2 = cirq.Circuit(cirq.Moment(cirq.X(q0), cirq.Y(q1)))
```
- EARLIEST (default) packs ops into the earliest moment without conflicts.
- Explicit Moments pin parallelism, important for hardware timing and for noise per moment.

## Gotchas
- Operations in one Moment must act on disjoint qubits.

## Self-check
Compare len(circuit) for EARLIEST vs NEW.
