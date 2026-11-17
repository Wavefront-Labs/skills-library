---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-qasm-syntax
name: qc-qasm-syntax
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [openqasm3-syntax, openqasm-3]
level: practitioner
status: draft
description: "Write OpenQASM 3 programs with qubit and bit declarations, standard gates, gate definitions and measurement."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenQASM 3 types, gates and registers
```
OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
gate bell a, b { h a; cx a, b; }
bell q[0], q[1];
c = measure q;
```
- Types: bit, int[n], uint[n], float[n], angle[n], bool, complex[float[n]], duration; constants with const.
- Differences from OpenQASM 2: qubit/bit replace qreg/creg, and include "stdgates.inc" replaces qelib1.inc.

## Gotchas
- Check which parts of the spec your backend actually accepts; support is partial.

## Self-check
Parse the program above with a qasm3 loader.
