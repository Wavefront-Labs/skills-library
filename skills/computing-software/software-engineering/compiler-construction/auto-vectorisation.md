---
id: computing-software.software-engineering.compiler-construction.auto-vectorisation
name: auto-vectorisation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, slp-vectorizer, loop-vectorizer, vectorization-remarks, auto-vectorization, polyhedral-model, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "SIMD codegen"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auto-vectorisation

Goal: understand vectorisation.
- Loop vectoriser needs countable loops with analysable dependences; SLP packs independent scalar ops.
- Remarks: `-Rpass=loop-vectorize -Rpass-missed=loop-vectorize`.
- Aliasing and floating-point reassociation block vectorisation.
Verify: remark shows vectorised loop with expected width.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
