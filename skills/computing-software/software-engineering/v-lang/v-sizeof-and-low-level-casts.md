---
id: computing-software.software-engineering.v-lang.v-sizeof-and-low-level-casts
name: v-sizeof-and-low-level-casts
category: computing-software
field: software-engineering
product: v-lang
tags: [v-sizeof-and-low-level-casts, pointers-and-unsafe, sizeof, offsetof, typeof, voidptr, packed, aligned, v-lang]
level: advanced
status: docs-checked
description: "V's sizeof and __offsetof, typeof(x).name, voidptr to reference casts, and the @[packed] and @[aligned] struct attributes for byte-level layouts."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sizeof, __offsetof, typeof and layout attributes

Goal: do byte-level work correctly.

- `sizeof(Type)` gives the size of a type in bytes; `sizeof(value)` gives the size of the value's V type. `__offsetof(Struct, field_name)` gives a field's byte offset.
- Docs example: for `struct Foo { a int; b int }`, `sizeof(Foo) == 8`, `__offsetof(Foo, a) == 0` and `__offsetof(Foo, b) == 4`.
- `typeof(x).name` gives a type name (docs example: `typeof(fnums).name` is `[3]int`).
- `voidptr` is mostly used for C interoperability. Cast it to a V reference with `user := &User(user_void_ptr)`; casting pointers is memory-unsafe, so wrap it in `unsafe`.
- `@[packed]` on a struct creates an unaligned layout that decreases memory footprint; the docs warn it may hurt performance or be prohibited on some CPU architectures, and recommend it where memory matters more than speed (embedded).
- `@[aligned]` on a struct or union sets a minimum alignment in bytes; it can only increase the default alignment, use `@[packed]` to decrease it.

Gotchas:
- Unaligned access on architectures that do not support it is the documented risk of `@[packed]`.

Verify: assert `sizeof(YourStruct)` against the expected byte count, as the docs example does.

## Checked

Confirmed against the "sizeof and __offsetof", "Memory-unsafe code", "Attributes" and "V and C" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: `isizeof`, `encoding.binary` and `encoding.hex` helper names, `vmemcpy` (not in the docs read), and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
