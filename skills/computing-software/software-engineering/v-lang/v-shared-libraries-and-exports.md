---
id: computing-software.software-engineering.v-lang.v-shared-libraries-and-exports
name: v-shared-libraries-and-exports
category: computing-software
field: software-engineering
product: v-lang
tags: [v-shared-libraries-and-exports, v-cross-compilation-and-backends, -shared, shared library, dll, so, dylib, export, ffi, cdylib, embed in c, v-lang]
level: advanced
status: draft
description: "Create .so, .dll or .dylib from V with -shared, export C-callable functions with @[export], and consume them from other languages."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building shared libraries with -shared

Goal: expose V code as a native library.

- `v -shared -o libmyv.so mylib.v` (`.dll` on Windows, `.dylib` on macOS).
- Export symbols: `@[export: 'my_add'] pub fn add(a int, b int) int { return a + b }`; without export, V mangles names (`mymod__add`).
- Use only C-compatible types in the public ABI: ints, floats, pointers, `&char`, structs marked with C layout.
- Memory: strings returned to C should be copied (`.clone()`) and freed by a V-provided `free_xxx` function or use `-gc none` carefully.
- Calling from Python: `ctypes.CDLL('./libmyv.so').my_add(1, 2)`; from C: declare `int my_add(int,int);` and link `-L. -lmyv`.
- Init: shared libs with GC/threads may require calling an init function (`_vinit` / `_vcleanup`, confirm).

Gotchas:
- V arrays and strings are not C types; marshal through pointers and lengths.
- Rebuild when changing the exported signature; there is no ABI stability tooling.

Verify: load the library from a tiny C or Python caller and print a result.
