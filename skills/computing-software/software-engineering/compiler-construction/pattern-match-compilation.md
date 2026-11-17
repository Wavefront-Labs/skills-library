---
id: computing-software.software-engineering.compiler-construction.pattern-match-compilation
name: pattern-match-compilation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, decision-tree-matching, exhaustiveness-checking, pattern-matrix, pattern-match-compilation, decision-trees, exception-handling-lowering, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "ML-style match"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiling pattern matching

Goal: compile `match` efficiently.
- Pattern matrix algorithm (Maranget) produces decision trees; exhaustiveness and redundancy checks on the same matrix.
- Avoid retesting scrutinee subterms.
- Guards require fallthrough edges.
Verify: non-exhaustive match warns with a counterexample.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
