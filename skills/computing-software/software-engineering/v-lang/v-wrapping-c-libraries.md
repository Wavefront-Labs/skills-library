---
id: computing-software.software-engineering.v-lang.v-wrapping-c-libraries
name: v-wrapping-c-libraries
category: computing-software
field: software-engineering
product: v-lang
tags: [v-wrapping-c-libraries, c-interop, wrapper, c library, bindings, module wrapper, ffi, raii, free method, sqlite wrapper, v-lang]
level: advanced
status: draft
description: "Package a C library as a V module with raw C declarations, safe wrappers, resource cleanup via free methods and tests."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wrapping a C library as a V module

Goal: expose a safe V API over C.

1. Put `#include`/`#flag` and raw `fn C.x()` declarations in a private file (`c.v`).
2. Create wrapper structs holding the handle: `pub struct Db { mut: h &C.sqlite3 }`.
3. Constructors return results: `pub fn open(path string) !Db { mut h := &C.sqlite3(0); if C.sqlite3_open(path.str, &h) != 0 { return error('open failed') } return Db{h} }`.
4. Methods convert strings and errors; `pub fn (mut d Db) close() { C.sqlite3_close(d.h) }` and encourage `defer { db.close() }`.
5. Vendor small C sources in `c/` with `#flag @VMODROOT/c/x.c` and ship `v.mod`.
6. Add tests exercising error paths and large inputs.

Gotchas:
- Finalisers are not guaranteed; document the close requirement.
- Thread-safety of the C lib must be mirrored in docs.

Verify: create, use, close and reopen in a test under valgrind/ASAN.
