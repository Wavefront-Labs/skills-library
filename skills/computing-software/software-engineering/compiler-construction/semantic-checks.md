---
id: computing-software.software-engineering.compiler-construction.semantic-checks
name: semantic-checks
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, control-flow-checks, definite-assignment, return-checks, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Static checks beyond types"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Semantic checks

Goal: catch more errors statically.
- Check `break` outside loop, missing returns, unreachable code, definite assignment, constant folding of obviously wrong operations.
- Report all errors with spans and notes.
- Keep warnings configurable.
Verify: test suite of invalid programs yields expected diagnostics.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
