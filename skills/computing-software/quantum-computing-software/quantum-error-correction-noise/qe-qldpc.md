---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-qldpc
name: qe-qldpc
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [qldpc-bosonic-codes]
level: sme
status: draft
description: "Know what qLDPC (for example bivariate bicycle) and bosonic cat or GKP codes aim to reduce."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# qLDPC and bosonic codes overview
- qLDPC codes target a better encoding rate than surface code at the cost of non-local connectivity.
- Bosonic codes (cat, GKP) encode a qubit in an oscillator, trading ancilla overhead for hardware complexity.

## Gotchas
- Result claims change fast; cite the paper and date.

## Self-check
Compare the rate k/n of a surface code with a published qLDPC code.
