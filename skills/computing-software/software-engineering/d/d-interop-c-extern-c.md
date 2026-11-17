---
id: computing-software.software-engineering.d.d-interop-c-extern-c
name: d-interop-c-extern-c
category: computing-software
field: software-engineering
product: d
tags: [d-interop-c-extern-c, interop, extern-c, c-interop, bindings, tostringz, importc, ffi, core-stdc, callbacks, d]
level: practitioner
status: docs-checked
description: "Bind C libraries with extern(C) declarations, map types (c_long, size_t, char*), toStringz, struct layout, callbacks, importC (dmd -P) and link flags."
sources:
  - https://dlang.org/spec/interfaceToC.html
  - https://dlang.org/spec/importc.html
  - https://dlang.org/spec/struct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling and exposing C: extern(C), bindings, strings and structs

Goal: call C from D and export D to C.

- Declare: `extern(C) nothrow @nogc int puts(const char*);` Types: `core.stdc.config` (`c_long`, `c_ulong`), `size_t`, `ptrdiff_t`; the C standard does not pin type sizes, so check them per platform.
- Strings: C to D `fromStringz(p)` or `p[0 .. strlen(p)]`; D to C `std.string.toStringz`; keep GC memory reachable while C holds the pointer (malloc a copy, keep a pointer on the stack or in static data, or register it with `core.memory.GC.addRoot`/`addRange`).
- Struct layout matches C when fields and `align` match; use `static assert(S.sizeof == N)`. Bit fields: struct members, or the `std.bitmanip.bitfields` library type. Unions as `union`; D does not declare variables of anonymous struct types (define a named, private struct).
- Callbacks: `extern(C) void cb(void* user) { ... }` passed as `&cb`; delegates have no C equivalent.
- Avoid binding by hand: ImportC imports or compiles `.c` files directly (it runs the C preprocessor automatically for `.c` files; `dmd -P<flag>` passes preprocessor flags); DStep and dpp (both libclang-based) generate bindings from headers; check code.dlang.org for existing bindings.
- Link: `-L-lm` / `-L-lsqlite3` or dub `libs "sqlite3"`; `lflags`.
- Export to C: declare D functions `extern(C)`; compile as a library (`-lib`, `-shared`). Only the C runtime is needed when the code is restricted to betterC.

Gotchas:
- D `char` is unsigned and maps to C `char`; D `real` maps to `long double`; `class`, slices (`type[]`), AAs and delegates have no C equivalent.
- The compiler checks `printf` format strings against the arguments.

Verify: link a small C library, call it, run under a sanitizer.

## Checked

Date 2026-11-02. Confirmed extern(C) linkage, type mapping, strings, ImportC and printf checking (Interfacing to C and ImportC specs). Removed the always-32-bit int, str ~ '\0', export extern(C) header, bool/char size and void* context claims; corrected GC root guidance and bit field wording.

Method: documentation only; no commands were run.
