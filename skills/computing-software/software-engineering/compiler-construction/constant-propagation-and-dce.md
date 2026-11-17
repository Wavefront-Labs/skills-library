---
id: computing-software.software-engineering.compiler-construction.constant-propagation-and-dce
name: constant-propagation-and-dce
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, sparse-conditional-constant-propagation, dead-code-elimination, constant-folding, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Classic optimisations"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Constant propagation and dead code elimination

Goal: optimise IR.
- Constant folding, SCCP over SSA, DCE based on liveness, branch simplification.
- Preserve side effects (division by zero, volatile).
- Run to a fixed point with other cleanups.
Verify: optimised IR runs the same with fewer instructions.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
