---
id: computing-software.software-engineering.compiler-construction.loop-optimisations
name: loop-optimisations
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, loop-invariant-code-motion, strength-reduction, loop-unrolling, loop-optimisation, inlining, common-subexpression-elimination, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Loops"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loop optimisations

Goal: speed up loops.
- Find natural loops (back edges), hoist invariants (LICM) when safe, induction variable strength reduction, unrolling, fusion/fission.
- Alias and exception safety limit hoisting.
- Profile-guided choices.
Verify: loop benchmark IR shows reduced work in the body.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
