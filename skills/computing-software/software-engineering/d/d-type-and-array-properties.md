---
id: computing-software.software-engineering.d.d-type-and-array-properties
name: d-type-and-array-properties
category: computing-software
field: software-engineering
product: d
tags: [d-type-and-array-properties, properties, type-properties, sizeof, stringof, mangleof, alignof, d]
level: intro
status: draft
description: "Inspect types with .sizeof, .alignof, .init, .stringof, .mangleof, .max and array .length .ptr .dup .reverse .sort properties."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Type properties: .init .sizeof .stringof .mangleof

Goal: query type metadata with built-in dotted properties.

- Every type: `.sizeof`, `.alignof`, `.init`, `.stringof`, `.mangleof`.
- Arithmetic types: `.min`, `.max`, floats also `.epsilon`, `.dig`, `.infinity`, `.nan`, `.mant_dig`.
- Arrays: `.length`, `.ptr`, `.dup` (mutable copy), `.idup` (immutable copy), `.capacity`; the old `.reverse`/`.sort` properties were removed, use `std.algorithm.sort` and `reverse`.
- Associative arrays: `.keys`, `.values`, `.length`, `.byKey`, `.byValue`, `.byKeyValue`, `.get`, `.remove`.
- Classes: `.classinfo`, `.tupleof`; structs: `.tupleof` gives a field tuple.
- `typeid(T)` returns TypeInfo.

Gotchas:
- `.stringof` output is not stable across compiler versions; use `__traits(identifier, x)` or `fullyQualifiedName!T` for code.
- Do not rely on the old array `.sort` property; call `std.algorithm.sort` instead.

Verify: `assert(int.sizeof == 4 && "x".dup.capacity >= 1);`
