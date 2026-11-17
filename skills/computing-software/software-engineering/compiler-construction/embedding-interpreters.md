---
id: computing-software.software-engineering.compiler-construction.embedding-interpreters
name: embedding-interpreters
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, embedded-scripting, lua-c-api, host-api-design, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Scripting hosts"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Embedding an interpreter

Goal: embed a scripting runtime.
- Stack-based C APIs (Lua) or handle-based APIs (V8, CPython); manage lifetime and errors across boundaries.
- Sandbox: limit memory, instructions, and exposed functions.
- Keep the host API versioned.
Verify: a script cannot exceed instruction and memory budgets.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
