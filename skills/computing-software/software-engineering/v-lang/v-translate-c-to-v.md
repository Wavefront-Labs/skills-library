---
id: computing-software.software-engineering.v-lang.v-translate-c-to-v
name: v-translate-c-to-v
category: computing-software
field: software-engineering
product: v-lang
tags: [v-translate-c-to-v, translating-c-to-v, v translate, c2v, translate c, c to v, port c code, v2c, v-lang]
level: advanced
status: draft
description: "Use v translate (c2v) to convert C sources to V, review the output, and handle macros, goto and unions manually."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# v translate: converting C code to V

Goal: port a C codebase incrementally.

- `v translate file.c` (or `v translate -o out.v file.c`) converts via the c2v tool (downloaded on first use; confirm).
- Preprocess includes with the right flags: `v translate -I include/ file.c`; macros are expanded by the C preprocessor first.
- Expect to fix: pointer arithmetic (`unsafe`), `goto`, bitfields, varargs, function pointers, `#define` constants (turn into `const`), and header-only inline functions.
- Strategy: translate leaf files first, compile as a V module, keep the rest in C via `#include`/`C.` interop, then migrate gradually.
- Run the original C test suite against the translated module for parity.

Gotchas:
- Output is mechanical and unidiomatic; refactor to V types (`[]T`, strings) afterwards.
- Translation of C++ is not supported.

Verify: the translated module builds and your existing tests pass.
