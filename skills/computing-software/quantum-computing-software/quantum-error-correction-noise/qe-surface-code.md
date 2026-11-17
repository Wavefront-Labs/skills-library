---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-surface-code
name: qe-surface-code
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [surface-code-decoding, surface-code]
level: sme
status: draft
description: "Describe surface code geometry, logical error scaling and decoders such as MWPM."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Surface code layout and decoding
- Distance-d rotated surface code uses d^2 data qubits and d^2-1 measure qubits; threshold about 1 percent in circuit-level models.
- Logical error rate falls as (p/p_th)^((d+1)/2) below threshold.
- Decoding: minimum-weight perfect matching via PyMatching on the detector graph.
```python
import stim, pymatching
c = stim.Circuit.generated("surface_code:rotated_memory_z", distance=3, rounds=3, after_clifford_depolarization=0.001)
```

## Gotchas
- Detector error models, not raw syndromes, are what decoders consume.

## Self-check
Sample logical error vs distance at p=0.001 and confirm suppression.
