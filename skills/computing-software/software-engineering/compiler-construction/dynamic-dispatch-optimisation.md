---
id: computing-software.software-engineering.compiler-construction.dynamic-dispatch-optimisation
name: dynamic-dispatch-optimisation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, vtable-dispatch, hidden-classes, polymorphic-inline-cache, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Fast method calls"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vtables, hidden classes, inline caches

Goal: speed up dispatch.
- Static languages: vtables/itables. Dynamic languages: hidden classes (shapes) with inline caches at call sites (monomorphic, polymorphic, megamorphic).
- Invalidate caches on shape change.
- Measure hit rates.
Verify: property-access benchmark improves.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
