---
id: computing-software.software-engineering.compiler-construction.error-recovery-strategies
name: error-recovery-strategies
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, panic-mode-recovery, error-productions, synchronisation-tokens, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Continue after errors"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parser error recovery

Goal: report many errors per run.
- Panic mode: skip to synchronisation tokens (`;`, `}`); error productions for common mistakes; insert-missing-token heuristics.
- Keep the AST usable for IDE features.
- Limit cascades.
Verify: a file with 3 independent errors reports 3 diagnostics.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
