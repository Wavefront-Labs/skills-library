---
id: computing-software.software-engineering.nim.generic-constraints-and-specialization
name: generic-constraints-and-specialization
category: computing-software
field: software-engineering
product: nim
tags: [generic-constraints-and-specialization, generics, type-class, constraint, sometype, ordinal, specialization, or-types, nim]
level: advanced
status: docs-checked
description: "Constrain generics with type classes, unions and concepts, and specialise behaviour for particular types."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type constraints and specialization

Goal: restrict and specialise generic code.

- Built-in type classes: `object`, `tuple`, `enum`, `proc`, `iterator`, `ref`, `ptr`, `var`, `distinct`, `array`, `set`, `seq`, `auto` (any type). Every generic type also creates a type class of its own name that matches any instantiation.
- Combine with the boolean operators: `type RecordType = (tuple or object)`; as a constraint, `proc onlyIntOrString[T: int|string](x, y: T)`. `onlyIntOrString("xy", 50)` is invalid because `T` cannot be both at once.
- Type classes are static checks that resolve to one type, not runtime types: `var foo: int | string = 2` fixes `foo` as `int`, so assigning a string later fails.
- A type class used directly as a parameter type makes the proc implicitly generic, instantiated once per unique combination of parameter types. A named type class binds once; `distinct` on it lets each parameter bind to a different type (bind many).
- Group constraints with `,` and stop propagation with `;`: `proc fn1[T; U, V: SomeFloat]()` leaves `T` unconstrained.
- `proc` and `iterator` type classes accept a calling convention pragma: `proc onlyClosure[T: proc {.closure.}](x: T)`.
- Specialise inside a body with `is`, which is evaluated during semantic analysis: `when not (Key is string):`.
- Constraints can be concepts (see the concept skills).

Gotchas:
- `var T` and `typedesc[T]` cannot be inferred in a generic instantiation, and `g[var int](v, i)` is also rejected.
- Use `;` to separate independent constraint definitions such as `[H; T: Foo[H]]`.

Verify: calling an `int|string` constrained proc with floats gives a type mismatch.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository, Generics chapter lines 5847-6290 read in full): type class table, `or`/`|` combination, bind once and bind many, constraint grouping, calling convention type classes, the `is` operator and the inference restrictions. Removed, because that chapter does not state them: the `SomeInteger`/`SomeNumber`/`Ordinal` list as built-in classes, the `compiles(...)` specialisation advice, the claim that a more specific overload wins over a generic one, and the `static: doAssert` error advice. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
