---
id: computing-software.software-engineering.compiler-construction.compile-time-evaluation
name: compile-time-evaluation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, constexpr-evaluation, const-folding-interpreter, staged-compilation, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "CTFE"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compile-time evaluation

Goal: run code at compile time.
- Interpreter inside the compiler evaluates constant expressions (C++ constexpr, Zig comptime, Rust const eval).
- Limits on recursion and side effects; deterministic results.
- Enables generics/reflection via types as values (Zig).
Verify: compile-time computed table equals runtime result.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
