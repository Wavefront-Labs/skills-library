---
id: computing-software.software-engineering.compiler-construction.closures-and-environments
name: closures-and-environments
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, closure-conversion, upvalues, captured-variables, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "First-class functions"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Closures and upvalues

Goal: implement closures.
- Capture the defining environment (tree-walker) or upvalues pointing to stack slots that are closed over when they leave scope (bytecode VM).
- Resolver determines which locals are captured.
- Test counters, loops capturing variables.
Verify: closures retain state independently.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
