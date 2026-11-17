---
id: computing-software.quantum-computing-software.quantum-algorithms.qa-period
name: qa-period
category: computing-software
field: quantum-computing-software
product: quantum-algorithms
tags: [period-finding, shor-factoring]
level: advanced
status: draft
description: "Reduce factoring to order finding and use phase estimation of modular multiplication."
sources:
  - https://github.com/Qiskit/textbook
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Period finding and order finding
- Pick a coprime to N; order r of a mod N from phase estimation of U|y> = |a y mod N>.
- Continued fractions recover s/r from the measured phase.
- Classical post-processing: if r even and a^(r/2) != -1 mod N, gcd(a^(r/2) +- 1, N) gives factors.
```python
from math import gcd
f = gcd(pow(a, r // 2, N) - 1, N)
```

## Gotchas
- Success is probabilistic; rerun with a new a.

## Self-check
Factor 15 with a=7 (order 4).
