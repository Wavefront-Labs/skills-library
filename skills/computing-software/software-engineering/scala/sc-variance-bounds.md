---
id: computing-software.software-engineering.scala.sc-variance-bounds
name: sc-variance-bounds
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-generics, variance-bounds]
level: advanced
status: draft
description: "Annotate +T/-T correctly, use upper/lower bounds and opaque types for zero-cost wrappers."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Variance, bounds and opaque types
- `class Box[+A]` covariant (producers); `Function1[-A, +B]`; mutable containers must be invariant.
- Lower bound `def prepend[B >: A](b: B)`, upper bound `[T <: Ordered[T]]`.
- Context bound `def max[T: Ordering](xs: List[T])` sugar for an implicit parameter.
- `opaque type UserId = Int` in an object gives a distinct type at compile time without boxing.
- Union (`A | B`) and intersection (`A & B`) types are Scala 3 only.
Verify: the compiler rejects a wrong-variance definition.
