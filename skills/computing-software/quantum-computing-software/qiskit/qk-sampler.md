---
id: computing-software.quantum-computing-software.qiskit.qk-sampler
name: qk-sampler
category: computing-software
field: quantum-computing-software
product: qiskit
tags: [sampler-v2, qiskit-primitives]
level: practitioner
status: draft
description: "Run circuits with SamplerV2 using PUBs, read classical register data and counts."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/Qiskit/qiskit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SamplerV2 and primitive unified blocks
```python
from qiskit.primitives import StatevectorSampler
sampler = StatevectorSampler()
res = sampler.run([(qc, None, 2048)]).result()   # PUB = (circuit, params, shots)
counts = res[0].data.meas.get_counts()
```
- Result data is per classical register name (meas by default), not a single counts dict.
- Circuits must contain measurements.

## Gotchas
- Run hardware circuits only after transpiling to the backend ISA.

## Self-check
Read counts for a Bell circuit and confirm only 00 and 11.
