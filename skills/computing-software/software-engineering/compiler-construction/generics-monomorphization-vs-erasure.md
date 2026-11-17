---
id: computing-software.software-engineering.compiler-construction.generics-monomorphization-vs-erasure
name: generics-monomorphization-vs-erasure
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, monomorphization, type-erasure, dictionary-passing, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Implementing polymorphism"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generics: monomorphization vs erasure

Goal: pick an implementation strategy.
- Monomorphization (C++, Rust) duplicates code per type: fast, big binaries. Erasure (Java) uses boxing and casts. Dictionary passing (Haskell type classes) passes operation tables. Hybrid (C# reifies in the runtime).
- Tradeoffs: compile time, code size, runtime speed, separate compilation.
Verify: benchmark and binary size for each approach on a generic container.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
