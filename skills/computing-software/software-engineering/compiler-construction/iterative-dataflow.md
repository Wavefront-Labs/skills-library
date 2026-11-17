---
id: computing-software.software-engineering.compiler-construction.iterative-dataflow
name: iterative-dataflow
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, gen-kill-sets, worklist-algorithm, lattice-fixpoint, dataflow-analysis, liveness-analysis, reaching-definitions, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Analysis framework"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Iterative dataflow framework

Goal: implement analyses.
- Define lattice, transfer functions (gen/kill), meet; iterate a worklist to a fixed point; forward vs backward.
- Liveness (backward), reaching definitions (forward), available expressions (forward, intersection).
- Use reverse postorder for speed.
Verify: results match hand analysis on a small CFG.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
