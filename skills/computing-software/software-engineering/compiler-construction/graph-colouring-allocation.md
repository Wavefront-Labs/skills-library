---
id: computing-software.software-engineering.compiler-construction.graph-colouring-allocation
name: graph-colouring-allocation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, interference-graph, chaitin-briggs, spilling, register-allocation, graph-coloring, linear-scan, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Classic allocator"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Graph-colouring allocation

Goal: allocate registers.
- Build interference graph from liveness; simplify, select with k colours; spill and rewrite when stuck; coalesce moves conservatively.
- Precoloured nodes for calling conventions.
- Expensive for JITs.
Verify: allocated code has no conflicting registers and spills are minimal.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
