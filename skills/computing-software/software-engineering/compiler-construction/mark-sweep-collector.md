---
id: computing-software.software-engineering.compiler-construction.mark-sweep-collector
name: mark-sweep-collector
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, mark-and-sweep, tricolor-marking, gc-roots, garbage-collection, mark-sweep, generational-gc, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Basic GC"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mark-sweep collector

Goal: implement a collector.
- Roots: stack, globals, open upvalues; mark with a gray worklist; sweep unmarked objects from an intrusive list.
- Trigger by bytes allocated with a growth factor.
- Stress test: GC on every allocation to find missing roots.
Verify: no leaks and no use-after-free under GC stress mode.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
