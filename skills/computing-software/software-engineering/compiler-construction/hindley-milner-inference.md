---
id: computing-software.software-engineering.compiler-construction.hindley-milner-inference
name: hindley-milner-inference
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, algorithm-w, unification, let-polymorphism, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Type inference"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hindley-Milner inference

Goal: infer types.
- Generate type variables, collect constraints, solve by unification with occurs check; generalise at `let`.
- Algorithm W (substitution) vs constraint-based with levels for efficiency.
- Add type classes or row polymorphism as extensions (confirm complexity).
Verify: `let id = fun x -> x in (id 1, id true)` typechecks.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
