---
id: computing-software.software-engineering.nim.wasm-and-embedded-targets
name: wasm-and-embedded-targets
category: computing-software
field: software-engineering
product: nim
tags: [wasm-and-embedded-targets, cross-compilation, wasm, webassembly, emscripten, wasi, embedded, standalone, microcontroller, arm-cortex, nim]
level: sme
status: docs-checked
description: "Compile Nim to WebAssembly with emscripten or wasi toolchains and to microcontrollers with --os:standalone."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/backends.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebAssembly and embedded targets

Goal: reach non-desktop targets.

- WebAssembly through Emscripten: the shipped `config/nim.cfg` has an `@if emscripten:` block that sets `cc = clang`, `clang.exe = "emcc"` and `clang.linkerexe = "emcc"` (and `--target=wasm64` for `wasm64`), so `-d:emscripten` selects the Emscripten toolchain. The compiler knows a `wasm32` CPU.
- Bare metal: `--os:standalone` is a known target OS. `-d:useMalloc` makes Nim use C's `malloc` and only works with `--mm:none`, `--mm:arc` or `--mm:orc`.
- `--exceptions:setjmp|cpp|goto|quirky` selects the exception implementation; `-d:noSignalHandler` disables the crash handler from `system.nim`.
- Any other toolchain (WASI, Cortex-M linker scripts, cross compilers) is configured by `--os`, `--cpu`, `--cc` and `<cc>.exe` settings as in the compiler guide's cross-compilation section.

Gotchas:
- Standard library parts that need an OS (files, sockets, threads) may be unavailable on bare targets; check each module.

Verify: the produced module loads and runs main on the target.

## Checked

2026-11-02. Confirmed against config/nim.cfg (emscripten block), compiler/platform.nim (`standalone`, `wasm32`), nimc.md (`useMalloc`, `noSignalHandler`) and advopt.txt (`--exceptions`, `--mm`). Removed: the invented emscripten flag set, WASI `-d:wasi`, the Cortex-M recipe, the nesper/Arduino references, output file types and the size claim for `goto`/`quirky`.
Method: documentation only; no commands were run.
