---
id: computing-software.software-engineering.v-lang.v-comptime-for-reflection
name: v-comptime-for-reflection
category: computing-software
field: software-engineering
product: v-lang
tags: [v-comptime-for-reflection, compile-time-programming, for, reflection, fields, methods, attrs, values, variants, v-lang]
level: advanced
status: docs-checked
description: "Iterate struct fields, methods, enum values, attributes and sum-type variants at compile time with $for and branch per item with $if."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compile-time reflection with $for

Goal: generate per-type code without runtime reflection. `$` prefixes compile-time ("comptime") operations; V has compile-time `if` and `for`.

- Iterate struct fields with `$for field in User.fields { ... }`. It also works with generic types (`T.fields`) and generic arguments (`param.fields` in `fn gen[T](param T)`).
- `$if field.typ is string { ... }` is decided at compile time, separately for each item (docs example prints `name is of type string`). `$if field.name.to_upper() == 'AGE'` also works: a `$if` condition can compare metadata, use `is`, `.starts_with()`, `.ends_with()`, `.contains()`, `.len`, and combine with `&&`, `||`, `!`.
- Each field's `.attrs` is an array of strings; `for attr in field.attrs` (or `for index, attr in field.attrs`) processes them at runtime.
- Enums: `$for e in Color.values` gives `e.name`, `e.attrs` and `e.value`.
- Struct attributes: `$for e in Foo.attributes` yields attribute records with `name`, `has_arg`, `arg`, `kind`.
- Sum types: `$for v in MySum.variants` with `$if v.typ is int { ... } $else $if v.typ is string { ... }`.
- Methods: `$for m in Foo.methods`, then branch on `m.return_type` and call with `foo.$method()`. `$for param in m.params` exposes `param.name` and `param.typ`.
- Type metadata expressions expose `.typ`, `.idx`, `.key_type`, `.value_type`, `.element_type`, `.pointee_type`, `.payload_type`, `.variant_types`; `$zero(Type)` and `$new(Type)` return a zero value or pointer to one.
- `$for` can also iterate `split`, `split_any` or `fields` of a compile-time-known string; the compiler unrolls the body.

Gotchas:
- Mutable locals stay runtime; using one in a compile-time condition is an error.
- Methods with `mut` pointer parameters need a matching mutable variable at the reflected call.

Verify: run a small struct through the loop and compare to the docs-style `// Output:` comments.

## Checked

Confirmed against the "Compile time reflection" section of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: the full `T.fields` member list (`is_pub`, `is_mut`, `is_shared` not shown), the claim that json/orm/toml are built on this, the compile-time/binary-size claim, and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
