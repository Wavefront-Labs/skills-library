---
id: computing-software.software-engineering.ada.parameter-modes
name: parameter-modes
category: computing-software
field: software-engineering
product: ada
tags: [ada, parameter-modes, ada-subprograms]
level: practitioner
status: draft
description: "Ada procedure/function parameters: in, out, in out, defaults, named association and function return rules."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parameter modes and named association
```ada
procedure Swap (A, B : in out Integer) is T : Integer := A; begin A := B; B := T; end;
function Area (W : Float; H : Float := 1.0) return Float is (W * H);
Swap (A => X, B => Y);
R := Area (H => 2.0, W => 3.0);
```
- Ada 2012 allows `in out` and `out` parameters on functions; SPARK still forbids them (side effects).
- Scalar `out` parameters are uninitialised on entry; read before write is a bug.
- Passing mechanism (copy vs reference) is chosen by the compiler for small types.
## Gotchas
- Aliasing of `in out` parameters can give implementation-dependent results.
## Self-check
Call Swap with the same variable twice and note the SPARK/GNAT aliasing warning.
