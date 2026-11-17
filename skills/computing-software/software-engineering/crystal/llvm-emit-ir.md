---
id: computing-software.software-engineering.crystal.llvm-emit-ir
name: llvm-emit-ir
category: computing-software
field: software-engineering
product: crystal
tags: [llvm-emit-ir, llvm-backend, llvm, llvm-ir, emit, assembly, object-file, bitcode, codegen, inspect-generated-code, crystal]
level: advanced
status: docs-checked
description: "Use crystal build --emit with llvm-ir, asm, obj and llvm-bc to write LLVM IR, assembly, object and bitcode files, plus --ll and --x86-asm-syntax."
sources:
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/compiler.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Emitting LLVM IR, assembly and objects

Goal: read what the compiler generates.

- `crystal build --emit <list> app.cr` takes a comma-separated list of the targets `asm`, `obj`, `llvm-bc` and `llvm-ir`.
- Files are named from the output name: `.s` for asm, `.ll` for llvm-ir, `.bc` for llvm-bc, and the target's object extension for obj (`.o` on Unix).
- `--ll` dumps `.ll` files to Crystal's cache directory.
- `--x86-asm-syntax att|intel` picks the X86 dialect for `--emit asm` (AT&T is the default).
- `--release` (equivalent to `-O3 --single-module`) shows optimised output; `--no-debug` skips debug info.

Gotchas:
- `-o` decides the base name for emitted files.

Verify: look for your method name in the emitted `.ll` file.

## Checked

2026-11-03. Confirmed against the compiler source: the `--emit` option and `EmitTarget` values (`asm`, `obj`, `llvm-bc`, `llvm-ir`), output file suffixes in `compiler.cr`, `--ll`, `--x86-asm-syntax`, `--release`, `--no-debug`.
Removed: tool recommendations (`opt`, `llc`, `llvm-dis`), the `switch` and `@GC_malloc` reading tips, "IR is large because of the prelude", the self-hosting remark and LLVM-version claims.
Method: documentation only; no commands were run.
