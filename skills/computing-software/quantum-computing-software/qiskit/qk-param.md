---
id: computing-software.quantum-computing-software.qiskit.qk-param
name: qk-param
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [parameterized-circuits]
level: practitioner
status: draft
description: "Use Parameter and ParameterVector then bind values at run time for sweeps and variational loops."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parameterized circuits
```python
from qiskit.circuit import Parameter, ParameterVector
theta = Parameter("theta"); qc.ry(theta, 0)
bound = qc.assign_parameters({theta: 0.3})        # returns a new circuit
v = ParameterVector("v", 4)
```
- Primitives accept parameter value arrays directly in the PUB, so transpile once and bind many times.
- bind_parameters was removed; use assign_parameters.

## Gotchas
- Parameter names must be unique within a circuit.

## Self-check
Sweep theta over 10 values with one transpiled circuit.
