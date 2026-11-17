---
id: computing-software.software-engineering.compiler-construction.rc-arc-and-escape-analysis
name: rc-arc-and-escape-analysis
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, refcount-optimisation, escape-analysis, stack-allocation, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Automatic management"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reference counting and escape analysis

Goal: manage memory without a tracing GC.
- ARC inserts retain/release; optimisations remove redundant pairs; cycles need weak references or cycle collectors.
- Escape analysis stack-allocates objects not leaving a function (Go, JVM).
- Compare to tracing GC pause behaviour.
Verify: allocation count drops in benchmarks after optimisation.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
