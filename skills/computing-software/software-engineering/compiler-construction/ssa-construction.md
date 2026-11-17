---
id: computing-software.software-engineering.compiler-construction.ssa-construction
name: ssa-construction
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, ssa-construction, phi-nodes, dominance-frontier, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Static single assignment"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSA form

Goal: build SSA.
- Compute dominators, dominance frontiers, insert φ-functions, rename variables; or use Braun et al. on-the-fly construction.
- SSA simplifies many optimisations (constant propagation, DCE, GVN).
- Destroy SSA before register allocation.
Verify: each variable has exactly one definition; φs at joins.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
