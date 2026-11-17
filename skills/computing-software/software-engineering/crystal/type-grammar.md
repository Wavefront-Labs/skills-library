---
id: computing-software.software-engineering.crystal.type-grammar
name: type-grammar
category: computing-software
field: software-engineering
product: crystal
tags: [type-grammar, type-inference, nilable-shorthand, tuple-type, proc-type, pointer-type, static-array, typeof, class-type, crystal]
level: practitioner
status: draft
description: "Write type expressions: unions, nilable ?, generics, tuples, named tuples, procs, pointers, static arrays and class types."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Type grammar and typeof

Goal: spell any type in an annotation.

- Union `A | B`; nilable `A?` equals `A | Nil`.
- Generic `Array(Int32)`, `Hash(String, Int32)`; metaclass `Int32.class`; self type `self`.
- Tuple `{Int32, String}`; NamedTuple `{a: Int32}`; Proc `Int32, String -> Bool` (shorthand) or `Proc(Int32, String, Bool)`.
- Pointer `Int32*` / `Pointer(Int32)`; StaticArray `Int32[4]` / `StaticArray(Int32, 4)`.
- `typeof(a, b)` gives the union of both at compile time and does not execute the expression.

Gotchas:
- `Foo?` binds tighter than `|`, so `Int32 | String?` is `Int32 | String | Nil`.
- `T.class` expressions in generic restrictions need `.class`, e.g. `x : T.class`.
- `x.class` is the runtime class, `typeof(x)` the compile-time type.

Verify: `crystal eval 'p typeof(->(a : Int32){ a.to_s })'`.
