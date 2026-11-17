---
id: computing-software.software-engineering.compiler-construction.cross-compilation-targets
name: cross-compilation-targets
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, target-triple, sysroot, cross-toolchain, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Multiple targets"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-compilation and target triples

Goal: build for other platforms.
- Target triple `arch-vendor-os-abi`; need sysroot headers/libs, linker, runtime; LLVM `--target=aarch64-linux-gnu --sysroot=...`.
- Test on emulators (QEMU user mode).
- Watch endianness and ABI differences.
Verify: cross-built binary runs under QEMU.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
