---
id: computing-software.software-engineering.nim.os-cpu-flags-and-toolchain
name: os-cpu-flags-and-toolchain
category: computing-software
field: software-engineering
product: nim
tags: [os-cpu-flags-and-toolchain, cross-compilation, os, cpu, arm, aarch64, mingw, toolchain, crosscompile, linux-arm, nim]
level: advanced
status: docs-checked
description: "Target another OS or CPU by setting --os and --cpu and pointing Nim at a cross C compiler."
sources:
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross compile with --os, --cpu and a toolchain

Goal: build binaries for another platform.

- Flags: `--os:SYMBOL` and `--cpu:SYMBOL` set the target OS and processor. Known OS names include `linux`, `windows`, `macosx`, `android`, `freebsd`, `standalone`; known CPUs include `i386`, `amd64`, `arm`, `arm64`, `riscv64`, `wasm32`.
- Cross-compiling needs a C compiler for the target: set `<os>.<cpu>.<cc>.exe` and `.linkerexe` in config, for example `arm.linux.gcc.exe = "arm-linux-gcc"` and `arm.linux.gcc.linkerexe = "arm-linux-gcc"` (nimc.md), or pass `--gcc.exe:` / `--gcc.linkerexe:` on the command line.
- Generate C for another machine instead: `nim c --cpu:i386 --os:linux --compileOnly --genScript myproject.nim` (the compiler guide's own example), then compile with that machine's toolchain.
- Put the settings in `config.nims` or `nim.cfg` (configuration files support `@if` conditions).

Gotchas:
- Delete or force (`-f`) nimcache when switching target or compiler.

Verify: the produced binary is for the target (inspect it with the platform's file tool).

## Checked

2026-11-02. Confirmed against advopt.txt (`--os`, `--cpu`, `--genScript`), nimc.md (cross-compilation section, `arm.linux.gcc.exe`, `-f`) and compiler/platform.nim (OS and CPU names). Removed: the mingw and aarch64 compiler names, the `--os:standalone --mm:none` claim, the macOS SDK and dynlib gotchas, the `nimble build` claim.
Method: documentation only; no commands were run.
