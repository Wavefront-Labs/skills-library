---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-qv
name: qe-qv
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [quantum-volume]
level: sme
status: draft
description: "Interpret quantum volume and newer system-level benchmarks such as layer fidelity and CLOPS."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quantum volume and layer fidelity
- Quantum volume 2^n: largest square random circuit of width n and depth n with heavy-output probability above 2/3.
- Layer fidelity and EPLG give per-layer metrics; CLOPS measures speed (circuit layer operations per second).

## Gotchas
- Headline numbers are vendor-run; treat them as device selection hints.

## Self-check
Explain why QV is capped by the shortest-lived qubit set in the square circuit.
