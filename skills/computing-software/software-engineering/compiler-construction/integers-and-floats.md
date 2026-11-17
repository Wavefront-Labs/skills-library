---
id: computing-software.software-engineering.compiler-construction.integers-and-floats
name: integers-and-floats
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, integer-overflow-semantics, ieee754-nan, constant-folding-fp, integer-overflow, floating-point-semantics, unicode-strings, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Arithmetic rules"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Integer and floating-point semantics

Goal: define and implement arithmetic precisely.
- Choose overflow behaviour (wrap, trap, saturate, UB); division by zero and shifts by width; IEEE 754 NaN, signed zero, rounding modes.
- Constant folding must match runtime results, including floats.
- Fast-math flags relax rules.
Verify: folded and runtime results agree on edge-case tests.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
