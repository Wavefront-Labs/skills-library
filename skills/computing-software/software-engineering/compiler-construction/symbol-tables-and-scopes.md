---
id: computing-software.software-engineering.compiler-construction.symbol-tables-and-scopes
name: symbol-tables-and-scopes
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, lexical-scope, symbol-table-stack, variable-resolution, symbol-table, scope-resolution, name-resolution, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Name binding"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Symbol tables and scope resolution

Goal: resolve names.
- Stack of scope maps; declare then define to catch self-reference in initialisers.
- Resolver pass computes variable depth/slot to avoid runtime lookups.
- Errors: undefined, duplicate, use before init, shadowing rules.
Verify: closure capturing resolves to the right binding.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
