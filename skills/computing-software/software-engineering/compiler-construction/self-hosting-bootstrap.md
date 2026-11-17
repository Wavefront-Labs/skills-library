---
id: computing-software.software-engineering.compiler-construction.self-hosting-bootstrap
name: self-hosting-bootstrap
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, stage0-stage1-stage2, bootstrap-chain, reproducible-compiler, bootstrapping-compiler, cross-compilation, self-hosting, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Compiler of itself"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Self-hosting and bootstrap stages

Goal: self-host safely.
- Stage0 compiles stage1, stage1 compiles stage2, compare stage2 and stage3 output for fixed point.
- Keep a minimal bootstrap path; document seed compiler versions.
- Reproducible builds help detect compromise.
Verify: stage2 and stage3 binaries are identical.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
