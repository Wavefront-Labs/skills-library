---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-projective
name: qf-projective
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [projective-measurement-observables, measurement-theory]
level: practitioner
status: draft
description: "Measure in arbitrary bases by rotating, and treat Hermitian observables via eigendecomposition."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Projective measurement and observables
An observable is Hermitian; outcomes are eigenvalues, projectors P_k=|k><k|.
```python
qc.h(0)            # measure in X basis: H then Z-measure
qc.sdg(0); qc.h(0) # measure in Y basis
```
- Expectation <O> = sum_k lambda_k P(k) = <psi|O|psi>.

## Gotchas
- Measuring Y needs S-dagger then H, not just H.

## Self-check
Measure |+> in the X basis and get 0 with probability 1.
