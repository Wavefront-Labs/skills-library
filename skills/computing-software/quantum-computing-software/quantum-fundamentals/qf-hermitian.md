---
id: computing-software.quantum-computing-software.quantum-fundamentals.qf-hermitian
name: qf-hermitian
category: computing-software
field: quantum-computing-software
product: quantum-fundamentals
tags: [hermitian-unitary-spectral]
level: practitioner
status: draft
description: "Check Hermitian and unitary matrices and use spectral decomposition to apply functions of operators."
sources:
  - https://github.com/Qiskit/textbook
  - https://qiskit.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hermitian, unitary and eigendecomposition
```python
w, v = np.linalg.eigh(H)                 # Hermitian
expH = v @ np.diag(np.exp(-1j * w)) @ v.conj().T   # e^{-iH}
assert np.allclose(expH.conj().T @ expH, np.eye(len(w)))
```
- Use eigh (Hermitian) not eig; scipy.linalg.expm also works.
- Unitary: U^dagger U = I; eigenvalues have unit modulus.

## Gotchas
- Non-Hermitian input to eigh gives silently wrong results (it reads one triangle).

## Self-check
Verify e^{-iHt} is unitary for a random Hermitian H.
