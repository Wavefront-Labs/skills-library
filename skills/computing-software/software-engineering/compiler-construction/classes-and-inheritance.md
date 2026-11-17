---
id: computing-software.software-engineering.compiler-construction.classes-and-inheritance
name: classes-and-inheritance
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, class-implementation, super-calls, method-binding, method-dispatch, vtable, inline-caching, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Object models"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Classes and inheritance

Goal: add classes.
- Instances hold a class pointer and fields table; methods bound to receivers create bound-method objects.
- `super` resolves from the superclass of the defining class (lexically), not the receiver.
- Initializers and `this` capturing.
Verify: inheritance tests with super chains pass.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
