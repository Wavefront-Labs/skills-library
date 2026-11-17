---
id: computing-software.software-engineering.compiler-construction.internal-vs-external-dsl
name: internal-vs-external-dsl
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, embedded-dsl-design, external-dsl, fluent-api, domain-specific-language, embedded-dsl, language-workbench, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Choosing DSL style"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Internal vs external DSLs

Goal: choose a DSL strategy.
- Internal DSLs reuse host syntax/tools (fluent APIs, macros) with limited syntax; external DSLs need a parser, checker and tooling but offer full freedom.
- Consider error messages, IDE support, debugging.
- Start small and iterate with users.
Verify: users complete representative tasks in the DSL.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
