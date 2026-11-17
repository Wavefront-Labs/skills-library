---
id: computing-software.software-engineering.compiler-construction.ast-node-design
name: ast-node-design
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, ast-nodes, source-spans, sum-types, ast, visitor-pattern, tree-walking, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Representing programs"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AST node design

Goal: design a usable AST.
- Sum types/enums per node kind; keep source spans for diagnostics; separate expression and statement types.
- Arena allocation or indices for cache-friendly trees.
- Don't encode parser quirks (parentheses) unless needed for formatting.
Verify: pretty-printer reproduces the program.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
