---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-dj
name: qa-dj
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [deutsch-jozsa, oracle-algorithms]
level: practitioner
status: draft
description: "Implement Deutsch-Jozsa and Bernstein-Vazirani with phase oracles and read the hidden string in one query."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deutsch-Jozsa and Bernstein-Vazirani
H on all inputs, oracle phase (-1)^f(x), H again, measure; all-zero outcome means constant (DJ), outcome is the secret string s (BV).
```python
qc.h(range(n)); qc.x(n); qc.h(n)        # ancilla in |->
for i, bit in enumerate(reversed(s)):
    if bit == "1": qc.cx(i, n)          # BV oracle f(x)=s.x
qc.h(range(n)); qc.measure(range(n), range(n))
```
- Classical needs up to 2^(n-1)+1 queries for DJ and n for BV; quantum needs one.

## Gotchas
- Reversed string handling follows Qiskit little-endian ordering.

## Self-check
Recover s="1011" with one query.
