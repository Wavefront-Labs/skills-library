---
id: computing-software.software-engineering.compiler-construction.lr-items-and-tables
name: lr-items-and-tables
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, lr0-items, lalr1-lookahead, parse-table-construction, lr-parsing, lalr, shift-reduce, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "How yacc works"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LR(0), SLR, LALR(1) tables

Goal: understand LR parser generators.
- Build item sets (closure/goto), compute FOLLOW or lookaheads, fill ACTION/GOTO tables.
- LALR(1) merges states with identical cores (what yacc/bison do).
- Table size vs power: SLR < LALR < LR(1).
Verify: a small expression grammar's table is built by hand and matches the tool.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
