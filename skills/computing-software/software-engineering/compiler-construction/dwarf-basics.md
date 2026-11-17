---
id: computing-software.software-engineering.compiler-construction.dwarf-basics
name: dwarf-basics
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, dwarf-dies, line-number-program, cfi-unwind, dwarf, debug-info, line-tables, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Debug formats"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DWARF basics

Goal: emit useful debug info.
- DIEs describe types/variables/functions; the line-number program maps addresses to source lines; CFI describes stack unwinding.
- Inspect with `readelf --debug-dump=info`, `llvm-dwarfdump`.
- LLVM `DIBuilder` creates metadata.
Verify: gdb shows source lines and variables for your compiled language.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
