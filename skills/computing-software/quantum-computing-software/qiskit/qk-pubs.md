---
id: computing-software.quantum-computing-software.qiskit.qk-pubs
name: qk-pubs
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [pub-broadcasting]
level: advanced
status: draft
description: "Understand how primitive unified blocks broadcast parameter and observable arrays into result shapes."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PUB shapes and broadcasting
- A PUB is (circuit, parameter_values, [observables], [shots or precision]).
- Parameter arrays have a trailing axis equal to number of parameters; leading axes are broadcast against observable array shapes.
```python
import numpy as np
vals = np.random.rand(4, 1, 3)       # 4x1 sweep, 3 params
obs = [[o1], [o2], [o3], [o4], [o5]] # shape (5,1)
# result evs shape: (4,5)
```
- One PUB with many sweeps is cheaper than many separate jobs.

## Gotchas
- Mismatched axes raise a broadcast error rather than silently reshaping.

## Self-check
Predict and verify the result shape before submitting.
