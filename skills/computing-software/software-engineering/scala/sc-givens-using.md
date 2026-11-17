---
id: computing-software.software-engineering.scala.sc-givens-using
name: sc-givens-using
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-implicits, givens-using]
level: advanced
status: gated
description: "Define type classes with given/using, understand implicit resolution and migrate from implicits."
sources: ["https://docs.scala-lang.org/scala3/reference/contextual/givens.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# given, using, extension and type classes
- `trait Show[A] { def show(a: A): String }`, `given Show[Int] with { def show(a: Int) = a.toString }`, `def print[A](a: A)(using s: Show[A]) = s.show(a)`. (gated: unconfirmed, source is paywalled or blocked)
- Scala 3 imports givens separately: `import mod.given`; `import mod.*` does not import them.
- Resolution looks in lexical scope, then the implicit scope of the types involved (companions).
- Conversions need `given Conversion[A, B]`; implicit conversions need an explicit language import.
- Scala 2: `implicit val`, `implicit def`, `implicit class` for extension methods.
Verify: `summon[Show[Int]]` finds the instance; missing instances produce a compile error.

## Checked

Date: 2026-11-02. Gated: given syntax confirmed in the Scala 3 reference; import-given rules, implicit scope and Conversion detail were not on the page.

Method: documentation only; no commands were run.
