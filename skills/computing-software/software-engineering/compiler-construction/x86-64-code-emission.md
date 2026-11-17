---
id: computing-software.software-engineering.compiler-construction.x86-64-code-emission
name: x86-64-code-emission
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, rex-prefix, modrm-sib, machine-code-emission, x86-64-encoding, arm64-backend, cranelift, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Emitting machine code"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# x86-64 instruction encoding

Goal: emit raw machine code.
- Encodings: REX, opcode, ModRM, SIB, displacement, immediate; verify with `objdump -D -b binary -mi386:x86-64`.
- Use an assembler library (e.g. Cranelift, asmjit, keystone) rather than hand-encoding in production.
- Know RIP-relative addressing.
Verify: emitted bytes disassemble to the intended instructions.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
