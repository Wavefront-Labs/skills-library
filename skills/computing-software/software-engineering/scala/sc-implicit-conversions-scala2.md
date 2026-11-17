---
id: computing-software.software-engineering.scala.sc-implicit-conversions-scala2
name: sc-implicit-conversions-scala2
category: computing-software
field: software-engineering
product: scala
tags: [scala, implicit-conversions-scala2]
level: advanced
status: docs-checked
description: "Read Scala 2 implicit parameters, implicit classes and views, and Scala 3 Conversion with its feature flag."
sources: ["https://docs.scala-lang.org/scala3/book/ca-implicit-conversions.html", "https://docs.scala-lang.org/scala3/guides/migration/migrating-to-3-3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicits vs givens
- Scala 2 implicit conversion from `S` to `T` is an implicit class taking one parameter of type `S`, an implicit value of function type `S => T`, or an implicit method; it needs `import scala.language.implicitConversions`.
- In Scala 3, `import Conversions.given` brings given conversions into scope (givens are not imported by `*`).
- `-explain` makes the compiler describe errors in more detail.
Verify: compile and read the `-explain` output for an ambiguity.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 book page Implicit Conversions and the migration page Migrating to Scala 3.3 (-explain). Removed as not confirmed: that the import is needed for `given Conversion` use, `-source:future` leftover-implicit check, implicit-scope resolution order.

Method: documentation only; no commands were run.
