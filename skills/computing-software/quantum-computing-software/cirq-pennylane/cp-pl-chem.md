---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-pl-chem
name: cp-pl-chem
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [pennylane-qchem]
level: advanced
status: draft
description: "Build molecular Hamiltonians with qml.qchem and run VQE with a basis-set choice."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quantum chemistry Hamiltonians
```python
symbols = ["H","H"]; coords = pnp.array([0,0,0,0,0,1.4])   # bohr
H, n_qubits = qml.qchem.molecular_hamiltonian(symbols, coords)
```
- Needs openfermion and backends installed with the qchem extras; units are atomic units unless stated.
- Compare VQE energy with Hartree-Fock and exact diagonalization.

## Gotchas
- Active-space and mapping (Jordan-Wigner) choices change qubit counts.

## Self-check
Reproduce H2 ground energy near -1.137 Hartree around bond length 0.74 Angstrom.
