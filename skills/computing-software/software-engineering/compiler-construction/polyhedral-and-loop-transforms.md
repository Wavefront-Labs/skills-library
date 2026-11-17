---
id: computing-software.software-engineering.compiler-construction.polyhedral-and-loop-transforms
name: polyhedral-and-loop-transforms
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, polly, loop-tiling, loop-interchange, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Loop nest transforms"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Polyhedral optimisation

Goal: reason about loop nests.
- Polyhedral model represents iteration spaces as integer polyhedra to legally tile, interchange and fuse; Polly (LLVM) and ISL implement it.
- Applies to affine loops with static control.
- Gains for cache locality and parallelism.
Verify: tiled matmul faster than naive on large sizes.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
