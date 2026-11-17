---
id: computing-software.software-engineering.compiler-construction.stack-vm-design
name: stack-vm-design
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, opcode-dispatch, constant-pool, call-frames, bytecode-vm, stack-vm, register-vm, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "VM core"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stack-based VM design

Goal: build a bytecode VM.
- Chunk = code bytes + constants + line table; opcodes like `OP_CONSTANT`, `OP_ADD`, `OP_JUMP_IF_FALSE`, `OP_CALL`.
- Dispatch with switch or computed goto; call frames hold ip and stack window.
- Locals as stack slots resolved at compile time.
Verify: disassembler output matches expected code for sample programs.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
