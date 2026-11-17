---
id: computing-software.software-engineering.d.d-betterc-embedding-and-library-use
name: d-betterc-embedding-and-library-use
category: computing-software
field: software-engineering
product: d
tags: [d-betterc-embedding-and-library-use, betterc, betterc-library, webassembly, wasm, bare-metal, embedded, ldc, extern-c-api, freestanding, d]
level: sme
status: draft
description: "Ship D as a C-compatible library or target wasm and bare metal with -betterC and LDC, exposing extern(C) APIs and avoiding druntime initialisation."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using BetterC for libraries, WebAssembly and embedded targets

Goal: write a small library callable from C, Python or a host app.

- Export `extern(C)` functions with plain types and pointers/`ptrdiff_t` lengths (slices are not C-ABI); write `struct Buf { ubyte* ptr; size_t len; }` for pairs.
- Build: `ldc2 -betterC -shared -O -of=libfoo.so foo.d` (Windows `-of=foo.dll`, mark `export`), or static `-lib`.
- No `rt_init` is needed in betterC; in normal D libraries, expose `extern(C) void foo_init() { import core.runtime; Runtime.initialize(); }` and the matching terminate for hosts that do not call D's main.
- WebAssembly (LDC): `ldc2 -mtriple=wasm32-unknown-unknown-wasm -betterC -Os -L-allow-undefined -of=a.wasm a.d` and supply imports (confirm exact flags for your LDC version).
- Embedded: `-mtriple=thumbv7em-none-eabi -betterC -mcpu=cortex-m4` plus your linker script and startup file.
- Generate headers by hand or with `dmd -HC` (C++ header generation for extern(C++), confirm).

Gotchas:
- Mixing druntime D with betterC objects in one binary needs the runtime linked once.
- Alignment and calling convention differences on ARM/WASM; test at the boundary.

Verify: call the library from a tiny C or Python (ctypes) harness and assert results.
