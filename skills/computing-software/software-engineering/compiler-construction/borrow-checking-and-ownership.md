---
id: computing-software.software-engineering.compiler-construction.borrow-checking-and-ownership
name: borrow-checking-and-ownership
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, borrow-checker, lifetimes, move-semantics, ownership-borrow-checking, reference-counting, escape-analysis, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Static memory safety"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ownership and borrow checking

Goal: understand ownership analysis.
- Track moves/borrows on the CFG with region/lifetime constraints (NLL in Rust solves with liveness-based regions).
- Reports errors for aliasing + mutation.
- Heavy to implement; start with simple linear types.
Verify: classic use-after-move and double-mutable-borrow examples are rejected.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
