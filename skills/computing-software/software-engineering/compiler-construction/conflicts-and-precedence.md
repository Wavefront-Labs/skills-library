---
id: computing-software.software-engineering.compiler-construction.conflicts-and-precedence
name: conflicts-and-precedence
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, shift-reduce-conflict, reduce-reduce-conflict, bison-precedence, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Resolving conflicts"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shift/reduce conflicts and precedence

Goal: resolve grammar ambiguity.
- Dangling else is a shift/reduce conflict; default shift is correct.
- `%left '+' '-'`, `%right '^'`, `%prec UMINUS` in bison.
- Reduce/reduce conflicts mean the grammar is genuinely ambiguous; refactor.
Verify: `bison -Wcounterexamples` shows no unresolved conflicts.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
