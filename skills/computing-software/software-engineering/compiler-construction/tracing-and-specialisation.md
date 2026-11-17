---
id: computing-software.software-engineering.compiler-construction.tracing-and-specialisation
name: tracing-and-specialisation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, trace-compilation, type-specialisation, guards-deopt, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Dynamic language speed"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracing JITs and specialisation

Goal: specialise on observed types.
- Trace hot loops, record operations, compile with type guards and side exits (LuaJIT, PyPy).
- Inline caches feed type feedback.
- Pitfalls: trace explosion, megamorphic sites.
Verify: numeric loop reaches near-native speed.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
