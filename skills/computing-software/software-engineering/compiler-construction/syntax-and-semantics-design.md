---
id: computing-software.software-engineering.compiler-construction.syntax-and-semantics-design
name: syntax-and-semantics-design
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, grammar-ambiguity, syntax-choices, semantic-specification, language-design, grammar-design, syntax-design, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Designing a language"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Syntax and semantics design

Goal: design a coherent language.
- Keep grammar LL(1)/LR-friendly; avoid ambiguity (dangling else, generics `<>`); decide on semicolons, whitespace, precedence tables.
- Write an informal spec plus executable tests; consider operational semantics.
- Prototype with an interpreter first.
Verify: example programs read well and parse without ambiguity.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
