---
id: computing-software.software-engineering.v-lang.v-choosing-c-compiler
name: v-choosing-c-compiler
category: computing-software
field: software-engineering
product: v-lang
tags: [v-choosing-c-compiler, v-cross-compilation-and-backends, -cc, tcc, gcc, clang, msvc, zig cc, c compiler, cflags, v-lang]
level: practitioner
status: draft
description: "Select tcc, gcc, clang, msvc or zig cc with -cc, understand speed vs optimisation tradeoffs and pass compiler flags."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing and configuring the C compiler (-cc)

Goal: use the right C backend per situation.

- Default dev compiler is bundled tcc on supported platforms (very fast compile, little optimisation). `-prod` switches to gcc/clang when found.
- Explicit: `v -cc gcc .`, `-cc clang`, `-cc cl` (MSVC; needs Visual Studio build tools), `-cc zig` or `zig cc` wrappers for cross targets (confirm).
- Extra flags: `-cflags "-O2 -Wall"`; `-ldflags "-L/opt/lib"`; sanitisers `-cflags -fsanitize=address` with `-cc clang`.
- `v -showcc` prints the exact compile line; `v -keep-c -o out.c` keeps C for inspection.
- Install gcc/clang through your OS package manager (build-essential on Debian; MSYS2/mingw-w64 or LLVM on Windows).

Gotchas:
- tcc lacks some builtins and SIMD; code that needs them must pick gcc/clang.
- Mixed compiler versions can break cached modules; `v wipe-cache` after switching.

Verify: `v -cc gcc -prod .` and run `file` on the binary.
