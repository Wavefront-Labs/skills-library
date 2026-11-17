---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-channels
name: qe-channels
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [pauli-depolarizing-amplitude-damping]
level: practitioner
status: draft
description: "Distinguish bit-flip, phase-flip, depolarizing, amplitude-damping and phase-damping channels and their Kraus forms."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Standard error channels
- Depolarizing p: rho -> (1-p) rho + p I/2 (convention-dependent parameter, check the library).
- Amplitude damping gamma: K0 = diag(1, sqrt(1-gamma)), K1 = [[0, sqrt(gamma)],[0,0]]; non-unital.
- Phase damping shrinks off-diagonals only.

## Gotchas
- Parameter conventions differ between libraries (p vs 4p/3).

## Self-check
Apply amplitude damping to |1> and observe population decay.
