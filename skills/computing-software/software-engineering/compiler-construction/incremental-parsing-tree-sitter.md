---
id: computing-software.software-engineering.compiler-construction.incremental-parsing-tree-sitter
name: incremental-parsing-tree-sitter
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, tree-sitter-grammar, incremental-reparse, error-tolerant-parsing, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Fast edits"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incremental parsing

Goal: reparse efficiently.
- Tree-sitter grammars (JS DSL) produce error-tolerant concrete syntax trees updated incrementally on edit.
- Used for highlighting, folding, structural navigation.
- Queries (`.scm`) capture nodes.
Verify: edits reparse in milliseconds on large files.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
