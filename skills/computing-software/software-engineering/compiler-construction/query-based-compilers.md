---
id: computing-software.software-engineering.compiler-construction.query-based-compilers
name: query-based-compilers
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, salsa-framework, demand-driven-compilation, memoization, incremental-compilation, query-based-compiler, build-cache, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Modern compiler structure"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Query-based architecture

Goal: structure a compiler for incrementality.
- Express compilation as memoised pure queries with dependency tracking (rustc, Salsa, Roslyn); on edit, recompute only invalidated queries.
- Design stable keys (IDs) and avoid global mutable state.
- Great for IDE responsiveness.
Verify: editing one function recomputes only dependent queries.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
