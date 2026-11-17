---
id: computing-software.software-engineering.compiler-construction.generational-and-copying-gc
name: generational-and-copying-gc
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, copying-collector, generational-gc, write-barrier, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Advanced GC"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Copying and generational GC

Goal: understand modern GCs.
- Semispace copying with Cheney's algorithm; generational hypothesis; write barriers/remembered sets for old-to-young pointers.
- Concurrent and incremental collectors trade throughput for pauses.
- Reference counting with cycle detection as an alternative.
Verify: benchmark pause times vs throughput.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
