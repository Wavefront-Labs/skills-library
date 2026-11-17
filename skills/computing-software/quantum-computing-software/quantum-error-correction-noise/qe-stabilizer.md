---
id: computing-software.quantum-computing-software.quantum-error-correction-noise.qe-stabilizer
name: qe-stabilizer
category: computing-software
field: quantum-computing-software
product: quantum-error-correction-noise
tags: [stabilizer-formalism]
level: advanced
status: draft
description: "Describe codes by commuting Pauli stabilizer generators and simulate Clifford circuits efficiently."
sources:
  - https://quantum.cloud.ibm.com/docs/
  - https://github.com/quantumlib/Stim
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stabilizer formalism and Gottesman-Knill
- [[n,k,d]] code with n-k independent commuting generators; syndromes are generator eigenvalues.
- Tableau simulators (CHP, Stim) handle Clifford circuits in polynomial time.
```python
import stim
c = stim.Circuit("H 0\nCNOT 0 1\nM 0 1"); print(c.compile_sampler().sample(5))
```

## Gotchas
- Generators must commute; X and Z type checks overlap on an even number of qubits.

## Self-check
Verify Bell state stabilizers XX and ZZ.
