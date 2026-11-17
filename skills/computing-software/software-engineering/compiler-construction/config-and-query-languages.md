---
id: computing-software.software-engineering.compiler-construction.config-and-query-languages
name: config-and-query-languages
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, expression-language, template-engine, sandboxed-evaluation, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Practical DSLs"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuration and query languages

Goal: build safe expression evaluators.
- Parse to an AST, type check, evaluate with resource limits; avoid `eval` on untrusted input.
- Total (terminating) languages (CEL, Starlark) fit config use.
- Provide good error spans.
Verify: malicious inputs cannot loop forever or touch host resources.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
