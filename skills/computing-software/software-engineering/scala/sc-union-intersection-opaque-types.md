---
id: computing-software.software-engineering.scala.sc-union-intersection-opaque-types
name: sc-union-intersection-opaque-types
category: computing-software
field: software-engineering
product: scala
tags: [scala, union-intersection-opaque-types]
level: advanced
status: docs-checked
description: "Use Scala 3 union types A | B, intersection A & B, and opaque type aliases for zero-cost domain types."
sources: ["https://docs.scala-lang.org/scala3/reference/new-types/union-types.html", "https://docs.scala-lang.org/scala3/reference/new-types/intersection-types.html", "https://docs.scala-lang.org/scala3/reference/other-new-features/opaques.html", "https://docs.scala-lang.org/scala3/book/scala-features.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Union, intersection, opaque types
- `def help(id: UserName | Password)` accepts either; pattern match on the value to handle each case. `A | B` is the same type as `B | A`.
- The compiler infers a union type for an expression only if it is given explicitly or the common supertype of the alternatives is transparent; otherwise the type is widened to the common supertype.
- `S & T` is the type of values that are both `S` and `T`: `def f(x: Resettable & Growable[String])` can call members of both.
- `opaque type Logarithm = Double` inside an object provides type abstraction without overhead; define the public API with companion `apply` and extension methods inside the defining scope.
- Opaque type aliases replace most uses of value classes, with no boxing.
Verify: using the underlying type where the opaque type is expected, outside the defining scope, fails to compile.

## Checked

Date: 2026-11-02. Confirmed on Scala 3 reference (Union Types, Intersection Types, Opaque Type Aliases) and the Scala 3 book feature list. Fixed: the skill said unions are not widened unless needed; the reference says a union is only inferred when explicitly given or the supertype is transparent. Removed: 'replaces A with B' and 'prefer opaque over value classes' wording.

Method: documentation only; no commands were run.
