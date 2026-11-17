---
id: computing-software.software-engineering.v-lang.v-c-strings-and-pointer-conversion
name: v-c-strings-and-pointer-conversion
category: computing-software
field: software-engineering
product: v-lang
tags: [v-c-strings-and-pointer-conversion, c-interop, c string, c literal, str, cstring_to_vstring, tos_clone, tos, char pointer, null terminated, v-lang]
level: advanced
status: docs-checked
description: "Convert between V strings and C char pointers with c'' literals, .str, vstring, vstring_with_len and cstring_to_vstring, avoiding lifetime bugs."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C strings and converting pointers

Goal: pass text across the boundary.

- To C: a string literal prefixed with `c`, as in `C.sqlite3_open(c'users.db', &db)`, is a C string, not a V string. From a V string use its `.str` field, the C-style zero-terminated representation: `&char(query.str)`.
- From C to V without copying: `unsafe { &char(cstring).vstring() }`, or `unsafe { &char(cstring).vstring_with_len(len) }` when the length is known. These do NOT copy, so do not free the C string after calling them.
- From C to V with a copy: `unsafe { cstring_to_vstring(cstring) }`; the docs say libc APIs such as `getenv` need a copy because they return pointers to internal libc memory.
- Windows wide (UTF-16) strings: `string_from_wide(&u16(cwidestring))`.
- Types for interop: `voidptr` for `void*`, `&u8` for `byte*`, `&char` for `char*`, `&&char` for `char**`.
- `const char *` parameters are redeclared with a `const_` name prefix, for example `const_format &char`.

Gotchas:
- Conversions are `unsafe`; a non-copying view is valid only while the C memory lives.
- Strings freed by C code must be released with the C library's own function (the sqlite example calls `C.sqlite3_free(error_msg)`).

Verify: round-trip a string through a redeclared `C.puts` or similar C function and print the result.

## Checked

2026-11-08. Read: the "Calling C from V" and "C types" sections of doc/docs.md (vlang/v). Removed unconfirmed claims: `tos`, `tos2`, `tos3` and `tos_clone` helpers, NUL-in-string truncation note, `C.snprintf` buffer recipe, `C.free(voidptr(p))` advice and the dangling `.str` temporary note. docs.vlang.io and modules.vlang.io dropped from sources.
Method: documentation only; no commands were run.
