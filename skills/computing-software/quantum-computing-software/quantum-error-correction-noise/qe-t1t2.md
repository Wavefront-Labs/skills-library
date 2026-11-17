---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-t1t2
name: qe-t1t2
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [t1-t2-decoherence, quantum-noise]
level: practitioner
status: draft
description: "Relate T1 relaxation, T2 dephasing and gate time to circuit error budgets."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# T1, T2 and decoherence
- T1: energy relaxation |1> to |0>; T2: dephasing, T2 <= 2 T1; 1/T2 = 1/(2 T1) + 1/T_phi.
- Rough decoherence error per gate = t_gate / T1 or T2; circuit duration must stay well under T2.
```python
backend.qubit_properties(0).t1, backend.qubit_properties(0).t2   # seconds
```
- Calibration data changes between jobs; query it fresh.

## Gotchas
- Mixing units (seconds vs microseconds) is the standard mistake.

## Self-check
Estimate the survival probability of a state after 100 two-qubit gates of 300 ns.
