---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-shor9
name: qe-shor9
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [shor-steane-code]
level: advanced
status: draft
description: "Compare the 9-qubit Shor code and the 7-qubit Steane CSS code."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shor nine-qubit and Steane codes
- Shor [[9,1,3]] concatenates bit-flip and phase-flip repetition; Steane [[7,1,3]] is CSS from the Hamming [7,4] code.
- Both correct any single-qubit error since X, Z and Y errors span the Pauli basis (error discretization).
- Steane supports transversal Clifford gates.

## Gotchas
- Corrects any single qubit error, not arbitrary multi-qubit errors.

## Self-check
Build Steane stabilizers from the Hamming parity-check matrix.
