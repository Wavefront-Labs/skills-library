---
id: computing-software.software-engineering.crystal.union-type-basics
name: union-type-basics
category: computing-software
field: software-engineering
product: crystal
tags: [union-type-basics, union-types, union-type, union, tagged-union, type-id, method-on-union, crystal]
level: practitioner
status: docs-checked
description: "Reason about Crystal union types: automatic unions, method-call rules, virtual types, tuple and named tuple unions."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/union_types.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Union type basics

Goal: reason about unions.

- The compiler creates unions automatically, e.g. a variable assigned `1` in one `if` branch and `"hello"` in the other is `Int32 | String`. At runtime it holds one type (`a.class`); the compile-time type is `typeof(a)`.
- A method call on a union compiles only if all members respond; the result type is the union of the return types (`a.to_s` is `String`; `a + 1` fails because `String#+(Int32)` is not defined).
- Force a compile-time union with `0.as(Int32 | Nil | String)`.
- Classes and structs in one hierarchy whose nearest common ancestor is not `Reference`, `Struct`, `Int`, `Float` or `Value` collapse to `Parent+` (a virtual type).
- Tuples of the same size merge position-wise: `Tuple(Int32 | Bool, String | Nil)`. Named tuples with the same keys (any order) merge per key.

Verify: `p typeof(x)` and `p x.class` while debugging a type error.

## Checked
Checked 2026-11-02 against the crystal-book Union types page. Removed: memory-layout claim, flattening/dedupe, `Int32 | Float64` staying a union remark, code-size and `Array(Int32 | String)` remarks.

Method: documentation only; no commands were run.
