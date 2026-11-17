---
id: computing-software.software-engineering.compiler-construction.module-systems-and-imports
name: module-systems-and-imports
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, import-resolution, module-graph, separate-compilation, module-system, monomorphization, generics-implementation, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Programs in many files"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Module systems and name visibility

Goal: compile multi-file programs.
- Build a module graph, resolve imports (detect cycles), export interfaces; per-module compilation units with interface files.
- Name mangling for symbols (Itanium ABI, Rust v0).
- Incremental compilation caches per-module results.
Verify: changing one module recompiles only dependents.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
