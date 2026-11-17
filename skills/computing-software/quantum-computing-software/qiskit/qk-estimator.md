---
id: computing-software.quantum-computing-software.qiskit.qk-estimator
name: qk-estimator
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [estimator-v2]
level: practitioner
status: draft
description: "Compute expectation values with EstimatorV2 using PUBs of circuit, observable, parameters and precision."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EstimatorV2 and observables
```python
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
est = StatevectorEstimator()
obs = SparsePauliOp("ZZ")
ev = est.run([(qc, obs, [[0.1],[0.2]])]).result()[0].data.evs
```
- Observables must be mapped to the transpiled layout: obs.apply_layout(isa_circuit.layout).
- precision argument replaces shots on hardware (V2).

## Gotchas
- Circuit must have no measurements for an Estimator.

## Self-check
Check evs shape matches broadcast of parameters and observables.
