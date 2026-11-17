---
id: computing-software.quantum-computing-software.cirq-pennylane.cp-cirq-params
name: cp-cirq-params
category: computing-software
field: quantum-computing-software
product: cirq-pennylane
tags: [cirq-parameter-sweeps, cirq-advanced]
level: practitioner
status: draft
description: "Use sympy symbols with ParamResolver and Sweepable to run parameter sweeps."
sources:
  - https://quantumai.google/cirq
  - https://docs.pennylane.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Symbols and ParamResolver sweeps
```python
import sympy
t = sympy.Symbol("t")
c = cirq.Circuit(cirq.rx(t).on(q0), cirq.measure(q0))
res = cirq.Simulator().run_sweep(c, cirq.Linspace("t", 0, 3.14, 5), repetitions=100)
```
- Sweeps: cirq.Points, cirq.Linspace, cirq.Product, cirq.Zip.

## Gotchas
- Rotation exponent conventions: cirq.rx takes radians, while XPowGate takes exponent of pi.

## Self-check
Verify the sweep returns 5 result objects.
