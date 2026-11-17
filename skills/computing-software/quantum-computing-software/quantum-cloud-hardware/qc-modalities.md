---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-modalities
name: qc-modalities
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [qubit-modalities, quantum-hardware]
level: intro
status: draft
description: "Compare superconducting, trapped-ion, neutral-atom, photonic and spin qubits for connectivity, speed and coherence."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Qubit modalities
- Superconducting: fast gates (tens of ns), fixed 2D connectivity, T1 around 100 us.
- Trapped ions: high fidelity, all-to-all in small chains, slower gates (microseconds to ms).
- Neutral atoms: reconfigurable arrays, Rydberg gates, scale to hundreds of qubits.
- Photonic: room-temperature options, measurement-based computing.

## Gotchas
- Order-of-magnitude figures only; numbers change per device generation.

## Self-check
Pick a modality for a circuit that needs all-to-all CNOTs.
