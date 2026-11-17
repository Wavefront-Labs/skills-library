---
id: computing-software.software-engineering.compiler-construction.calling-convention-details
name: calling-convention-details
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, sysv-amd64, register-arguments, stack-frame, calling-convention, abi, stack-frame-layout, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Function call lowering"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calling conventions in practice

Goal: lower calls correctly.
- SysV AMD64: integer args in rdi, rsi, rdx, rcx, r8, r9; floats in xmm0-7; return in rax/xmm0; callee-saved rbx, rbp, r12-r15; 16-byte stack alignment at call. Windows x64 differs (rcx, rdx, r8, r9, shadow space) - confirm against the ABI document.
- Large structs pass by hidden pointer or memory.
Verify: your code calls and is called by C compiled code.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
