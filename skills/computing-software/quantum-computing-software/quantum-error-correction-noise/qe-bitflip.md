---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-bitflip
name: qe-bitflip
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [repetition-code, quantum-error-correction]
level: practitioner
status: draft
description: "Encode against bit flips with 3 qubits, extract syndromes and correct, and see why it fails for phase errors."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three-qubit repetition codes
```python
qc.cx(0,1); qc.cx(0,2)               # encode a|0>+b|1> -> a|000>+b|111>
qc.cx(0,3); qc.cx(1,3); qc.cx(1,4); qc.cx(2,4)   # syndrome ancillas
```
- Syndrome 11 on (s1,s2) flags the middle qubit etc.; correct by lookup.
- Phase-flip code conjugates this with Hadamards.

## Gotchas
- Measuring data qubits directly destroys the state; measure only ancilla parities.

## Self-check
Inject each single X error and verify recovery.
