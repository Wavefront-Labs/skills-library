---
id: computing-software.software-engineering.compiler-construction.state-machine-transform
name: state-machine-transform
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, async-state-machine, generator-lowering, continuation-passing, coroutines, async-await-lowering, state-machine-transform, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "CPS and state machines"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Async/await to state machines

Goal: lower async functions.
- Transform suspension points into states in a struct holding locals; resume dispatches via switch; generators are the same shape.
- CPS conversion is an alternative; stackful coroutines switch stacks instead.
- Memory layout matters for size.
Verify: a generator yields the expected sequence.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
