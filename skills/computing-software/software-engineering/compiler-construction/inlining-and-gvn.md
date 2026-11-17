---
id: computing-software.software-engineering.compiler-construction.inlining-and-gvn
name: inlining-and-gvn
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, function-inlining, global-value-numbering, tail-call-elimination, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Interprocedural and redundancy"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inlining and value numbering

Goal: remove call overhead and redundancy.
- Inline small or hot callees using a cost model; value numbering eliminates redundant computations; tail-call elimination rewrites self-recursion to loops.
- Code size growth must be bounded.
- Beware recursion cycles.
Verify: inlined hot path no longer calls the function in the dump.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
