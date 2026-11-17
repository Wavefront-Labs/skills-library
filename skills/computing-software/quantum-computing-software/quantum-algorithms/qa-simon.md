---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-simon
name: qa-simon
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [simons-algorithm]
level: advanced
status: draft
description: "Find the hidden XOR mask s of a 2-to-1 function with O(n) quantum queries and classical linear algebra."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Simon's algorithm
- Prepare H on n qubits, apply U_f, measure the output register, H again and measure input: each result y satisfies y.s = 0 mod 2.
- Collect about n-1 independent y vectors, solve the linear system over GF(2) for s.
```python
# after sampling: nullspace of Y over GF(2); a quick check
assert all(bin(y & s).count("1") % 2 == 0 for y in ys)
```
- Exponential separation from classical in the oracle model; inspired Shor.

## Gotchas
- Repeat until the y vectors have rank n-1; random duplicates are common.

## Self-check
Recover a 3-bit s from sampled y values.
