---
id: computing-software.software-engineering.compiler-construction.reading-writing-llvm-ir
name: reading-writing-llvm-ir
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, llvm-ir-syntax, getelementptr, llvm-types, llvm, llvm-ir, llvm-opt, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "The IR language"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading and writing LLVM IR

Goal: read and emit IR.
- Typed SSA: `%r = add i32 %a, %b`, `define i32 @f(i32 %x) { entry: ret i32 %x }`; `alloca/load/store` for mutable locals (mem2reg promotes).
- `getelementptr` computes addresses only (no memory access); opaque pointers (`ptr`) in recent versions.
- Generate with `clang -S -emit-llvm -O0`, check with `opt -verify`.
Verify: `llc` compiles your IR and the program runs.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
