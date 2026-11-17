---
id: computing-software.software-engineering.compiler-construction.visitors-and-tree-transforms
name: visitors-and-tree-transforms
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, visitor-pattern-ast, tree-rewrite, pattern-matching-ast, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Traversal"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visitors and tree transformations

Goal: traverse and rewrite trees.
- Visitor pattern (OO) or pattern matching (FP) to implement passes; return new trees rather than mutating when possible.
- Generate boilerplate from a node description.
- Keep passes separate (resolve, check, lower).
Verify: each pass has tests on tiny trees.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
