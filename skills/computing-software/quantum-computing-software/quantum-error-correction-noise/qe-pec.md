---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-pec
name: qe-pec
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [probabilistic-error-cancellation]
level: sme
status: draft
description: "Invert a learned noise model by quasi-probability sampling and track the sampling overhead."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Probabilistic error cancellation
- Represent ideal operation as a signed combination of noisy implementable operations; sample and reweight.
- Sampling overhead gamma^2 per layer product, exponential in depth.
- Requires a precise noise model (e.g. sparse Pauli-Lindblad learning).

## Gotchas
- Drift in the noise makes the cancelled bias return.

## Self-check
Estimate overhead for a circuit of 50 two-qubit gates at gamma 1.05.
