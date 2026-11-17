---
id: computing-software.quantum-computing-software.qiskit.qk-testing
name: qk-testing
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [qiskit-testing-practice]
level: practitioner
status: draft
description: "Unit test circuits with exact operator checks, seeded simulators and statistical tolerances."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing quantum code
```python
from qiskit.quantum_info import Operator
assert Operator(my_circuit).equiv(Operator(expected))
sim = AerSimulator(seed_simulator=1234)
```
- Compare counts with a chi-squared or tolerance test, not equality.
- Test on small sizes with exact statevectors, then run integration with noise models.

## Gotchas
- Unseeded sampling makes flaky tests.

## Self-check
Write a test that fails if the Bell circuit loses its cx.
