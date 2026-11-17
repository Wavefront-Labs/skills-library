---
id: computing-software.software-engineering.v-lang.v-references-and-pointers
name: v-references-and-pointers
category: computing-software
field: software-engineering
product: v-lang
tags: [v-references-and-pointers, pointers-and-unsafe, reference, pointer, t, address of, dereference, nil, heap, v-lang]
level: practitioner
status: docs-checked
description: "Use &T references, take addresses with &, dereference with *, write nil as unsafe { nil }, and choose between &T and mut receivers."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# References, &T and automatic dereferencing

Goal: share data by reference.

- Take an address with `&`: `mut ref := &i`; allocate with `&Point{x: 1}`. Dereference with `*ref`, as in C.
- Fields are read through a reference without extra syntax (`foo.abc` for `foo &Foo`).
- An immutable parameter may be passed by value or by reference at the compiler's choice; write `&` (for example the receiver `fn (foo &Foo) bar()`) to force a reference. It is still immutable; use `mut foo Foo` to modify it.
- Comparing immutable reference parameters with `==` or `!=` compares addresses, not fields; dereference both (`*a == *b`) to compare values.
- Arguments of primitive types cannot be modified via `mut`; only complex types such as arrays and maps.
- A null reference is written `unsafe { nil }`: outside `unsafe` the compiler rejects direct `nil`, `0` and `voidptr(0)` where a non-option reference is expected. A reference field needs an initial value unless declared with a default such as `b &Node = unsafe { nil }`.
- Recursive types use references, e.g. `struct Node[T] { val T; left &Node[T] }`.
- Pointer arithmetic and pointer indexing are only allowed inside `unsafe`.

Verify: take `mut ref := &i`, change `i`, and assert `*ref` shows the new value.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "References", "Closures", "Mutable arguments", "Memory-unsafe code", "Structs with reference fields"). Removed: `fn bump(mut n int)` (the docs say primitive arguments cannot be modified), `fn bump(n &int)`, the `?&T` maybe-absent advice and heap-promotion and `@[heap]` remarks (only partly covered), and the voidptr arithmetic gotcha.

Method: documentation only; no commands were run.
