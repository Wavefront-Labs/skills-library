---
id: computing-software.software-engineering.crystal.typeof-sizeof-introspection
name: typeof-sizeof-introspection
category: computing-software
field: software-engineering
product: crystal
tags: [typeof-sizeof-introspection, alias-types, typeof, sizeof, instance-sizeof, offsetof, pointerof, introspection, memory-layout, crystal]
level: advanced
status: draft
description: "Use compile-time introspection operators to get types, byte sizes, field offsets and variable addresses."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# typeof, sizeof, instance_sizeof, offsetof, pointerof

Goal: inspect memory layout.

- `typeof(a, b)` union type of expressions (not evaluated).
- `sizeof(Int64)` = 8 bytes for a value; for a class `sizeof(Foo)` is the pointer size, `instance_sizeof(Foo)` the heap object size including the type id header.
- `offsetof(Foo, @x)` offset of an ivar in bytes.
- `pointerof(x)` returns a `Pointer(T)` to a local or ivar; use for C out-parameters.
- `x.object_id`, `x.crystal_type_id` for identity and type tag.

Gotchas:
- `pointerof` on a local that is captured by a closure points to the heap box.
- Unions add a type id word, so `sizeof(Int32 | Nil)` is bigger than 4.
- Pointers are unsafe; no bounds checks.

Verify: print `sizeof` values for your struct and compare to the C header's `sizeof`.
