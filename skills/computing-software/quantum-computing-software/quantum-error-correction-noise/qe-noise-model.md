---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-noise-model
name: qe-noise-model
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [aer-noise-model]
level: practitioner
status: draft
description: "Create a NoiseModel with depolarizing, thermal relaxation and readout errors and attach it to a simulator."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building noise models in Aer
```python
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
nm = NoiseModel()
nm.add_all_qubit_quantum_error(depolarizing_error(0.01, 2), ["cx"])
nm.add_all_qubit_readout_error(ReadoutError([[0.98, 0.02], [0.03, 0.97]]))
sim = AerSimulator(noise_model=nm)
```
- Noise model keys name the basis gates after transpile; add errors on the ISA gates.

## Gotchas
- Errors only fire for gates present in the transpiled circuit.

## Self-check
Show Bell-state wrong-parity counts increase with the cx error.
