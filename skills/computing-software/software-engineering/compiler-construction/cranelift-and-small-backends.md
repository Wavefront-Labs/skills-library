---
id: computing-software.software-engineering.compiler-construction.cranelift-and-small-backends
name: cranelift-and-small-backends
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, cranelift-codegen, qbe-backend, tcc-backend, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Alternative backends"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cranelift and other lightweight backends

Goal: choose a backend.
- Cranelift (fast compile, used by Wasmtime/rustc backend), QBE (simple SSA backend), TCC (single-pass C), LLVM (best optimisation, slower).
- Trade compile time for code quality.
- Evaluate IR and API ergonomics.
Verify: compile-time vs runtime benchmark on your language.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
