---
id: computing-software.software-engineering.compiler-construction.calling-conventions-and-abi
name: calling-conventions-and-abi
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, system-v-abi, stack-frame-layout, callee-saved, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Function calls"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calling conventions and ABI

Goal: generate ABI-correct code.
- Know argument registers, return registers, callee-/caller-saved sets, stack alignment (16 bytes on x86-64 SysV), red zone, varargs rules.
- Windows x64 differs (shadow space).
- Prologue/epilogue and frame pointers aid debugging.
Verify: your code interoperates with C code in both directions.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
