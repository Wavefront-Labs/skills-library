---
id: computing-software.software-engineering.scala.sc-enums-adt
name: sc-enums-adt
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-classes, enums-adt]
level: practitioner
status: docs-checked
description: "Model sums and products with Scala 3 enums and case classes and use exhaustive matching."
sources: ["https://docs.scala-lang.org/scala3/reference/enums/enums.html", "https://docs.scala-lang.org/scala3/book/taste-modeling.html", "https://docs.scala-lang.org/tour/pattern-matching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums and algebraic data types
- Scala 3: `enum Color: case Red, Green, Blue`; cases with parameters make an ADT, e.g. `enum Nat: case Zero; case Succ(pred: Nat)`.
- Scala 2 style: `sealed trait Shape; final case class Circle(r: Double) extends Shape`.
- A `match` on a `sealed` base type is checked for exhaustiveness by the compiler.
- Enums have `values`, `valueOf` and `ordinal`, can define methods in the enum body, and extend `scala.reflect.Enum`.
Verify: remove a case from a match and read the compiler warning.

## Checked

Date: 2026-11-02. Confirmed on Scala 3 reference (enums: values, valueOf, ordinal, methods, scala.reflect.Enum), Scala 3 book (enum and ADT syntax), Tour of Scala (sealed exhaustivity). Removed as not confirmed: the brace-syntax `Opt[+T]` example, the one-file rule for sealed hierarchies, enums implementing traits.

Method: documentation only; no commands were run.
