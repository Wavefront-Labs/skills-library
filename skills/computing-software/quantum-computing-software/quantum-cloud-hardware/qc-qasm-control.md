---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-qasm-control
name: qc-qasm-control
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [openqasm3-control-flow]
level: practitioner
status: draft
description: "Use if, for, while, subroutines (def) and extern functions with real-time classical values."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Classical control flow in OpenQASM 3
```
def parity(bit[2] r) -> bit { return r[0] ^ r[1]; }
bit c = measure q[0];
if (c == 1) { x q[1]; }
for uint i in [0:3] { h q[i]; }
```
- def defines classical or quantum subroutines; extern declares host functions.
- Box and delay set timing semantics (box marks a scheduled region).

## Gotchas
- Dynamic features are optional on hardware; unsupported control flow is rejected at compile time.

## Self-check
Write a repeat-until-success loop and run it on a simulator.
