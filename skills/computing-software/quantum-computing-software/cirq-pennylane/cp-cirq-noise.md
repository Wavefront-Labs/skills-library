---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-cirq-noise
name: cp-cirq-noise
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [cirq-noise-models]
level: advanced
status: draft
description: "Add noise channels such as depolarize and bit_flip, or whole-circuit noise models, and simulate with density matrices."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cirq noise models
```python
noisy = c.with_noise(cirq.depolarize(0.01))
rho = cirq.DensityMatrixSimulator().simulate(noisy_no_meas).final_density_matrix
```
- Single channels: cirq.depolarize, amplitude_damp, phase_damp, bit_flip.
- Insert channels explicitly for per-gate error.

## Gotchas
- with_noise puts noise after every moment, including single-qubit ones.

## Self-check
Check purity less than 1 after noise.
