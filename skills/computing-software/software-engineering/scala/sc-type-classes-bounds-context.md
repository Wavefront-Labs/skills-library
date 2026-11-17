---
id: computing-software.software-engineering.scala.sc-type-classes-bounds-context
name: sc-type-classes-bounds-context
category: computing-software
field: software-engineering
product: scala
tags: [scala, type-classes-bounds-context]
level: advanced
status: docs-checked
description: "Declare Scala type class constraints with context bounds [A: Ordering] and write type lambdas and match types in Scala 3."
sources: ["https://docs.scala-lang.org/scala3/book/ca-context-bounds.html", "https://docs.scala-lang.org/scala3/reference/new-types/type-lambdas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context bounds
- A bound like `: Ord` on a type parameter `A` of a method or class indicates a context parameter of type `Ord[A]`: `def maxElement[A: Ord](as: List[A]): A` is shorthand for a method with such a context parameter.
- Scala 3 type lambdas are written with `=>>`, e.g. `[X, Y] =>> Map[Y, X]`.
Verify: calling `maxElement` without a given `Ord` in scope fails to compile.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 book page Context Bounds and the Scala 3 reference page Type Lambdas. Removed as not confirmed: the `Ordering`/`summon` example, the Scala 2 kind-projector encoding, the match-type example.

Method: documentation only; no commands were run.
