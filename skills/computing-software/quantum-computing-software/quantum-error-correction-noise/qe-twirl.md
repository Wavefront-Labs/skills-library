---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-twirl
name: qe-twirl
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [twirling-dynamical-decoupling]
level: advanced
status: draft
description: "Randomize coherent errors with Pauli twirling and suppress idle dephasing with dynamical decoupling sequences."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pauli twirling and dynamical decoupling
- Twirling converts coherent noise into stochastic Pauli noise, which averages and mitigates better.
- DD inserts X-X or XY4 pulse trains in idle windows (via scheduling passes).
```python
# options.dynamical_decoupling.enable = True; options.twirling.enable_gates = True
```

## Gotchas
- DD only helps on idles; dense circuits gain little.

## Self-check
Compare a spin-echo T2 with and without DD.
