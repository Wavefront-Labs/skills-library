---
id: computing-software.software-engineering.compiler-construction.type-checker-basics
name: type-checker-basics
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, type-environment, typing-rules, subtyping, type-checking, hindley-milner, type-inference, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Static typing"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Type checkers

Goal: implement a type checker.
- Environment Γ maps names to types; implement rules like `Γ ⊢ e1 + e2 : int` as recursive functions; subtyping via a `subtype(a,b)` relation.
- Bidirectional checking (infer/check modes) gives better errors and handles annotations.
- Generics: substitute type parameters at instantiation.
Verify: ill-typed programs rejected with clear messages.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
