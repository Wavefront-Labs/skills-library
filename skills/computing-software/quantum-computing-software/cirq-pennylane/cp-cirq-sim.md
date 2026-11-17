---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-cirq-sim
name: cp-cirq-sim
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [cirq-simulator]
level: practitioner
status: draft
description: "Run cirq.Simulator for final states and repetitions, and use DensityMatrixSimulator for noise."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cirq simulation and sampling
```python
sim = cirq.Simulator()
res = sim.run(c, repetitions=1000); print(res.histogram(key="m"))
state = sim.simulate(c_no_measure).final_state_vector
```
- simulate returns the final state, run returns samples; measurements stop simulate being unitary.

## Gotchas
- Use qubit_order argument for consistent state vector indexing.

## Self-check
Confirm histogram keys 0 and 3 only for a Bell circuit.
