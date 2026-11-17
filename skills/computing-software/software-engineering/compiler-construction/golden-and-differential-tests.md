---
id: computing-software.software-engineering.compiler-construction.golden-and-differential-tests
name: golden-and-differential-tests
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, golden-tests, filecheck-lit, differential-compiler-testing, compiler-testing, differential-testing, csmith, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Test strategies"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Golden, snapshot and differential tests

Goal: build a test suite.
- Golden outputs for IR/diagnostics; LLVM `lit` + `FileCheck`; run the same program through interpreter and compiler and compare.
- Keep minimal repros for every bug.
- Run under sanitizers.
Verify: CI fails on a deliberately broken pass.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
