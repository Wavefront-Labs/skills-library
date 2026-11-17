---
id: computing-software.software-engineering.compiler-construction.fuzzing-and-reduction
name: fuzzing-and-reduction
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, program-generators, csmith-yarpgen, creduce, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Finding miscompilations"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fuzzing and test-case reduction

Goal: find compiler bugs.
- Generate valid programs (Csmith/YARPGen), compare optimisation levels or compilers; reduce failures with C-Reduce/`llvm-reduce`/delta debugging.
- Grammar-based fuzzers for parsers.
- Triage into frontend vs optimiser bugs.
Verify: a seeded bug is found and reduced to a small file.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
