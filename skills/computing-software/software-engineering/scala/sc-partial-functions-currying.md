---
id: computing-software.software-engineering.scala.sc-partial-functions-currying
name: sc-partial-functions-currying
category: computing-software
field: software-engineering
product: scala
tags: [scala, partial-functions-currying]
level: practitioner
status: docs-checked
description: "Use multiple parameter lists, PartialFunction with collect, and eta-expansion of methods to functions."
sources: ["https://docs.scala-lang.org/scala3/book/fun-partial-functions.html", "https://docs.scala-lang.org/scala3/book/fun-eta-expansion.html", "https://docs.scala-lang.org/scala3/book/control-structures.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Currying and partial functions
- A `PartialFunction` is checked with `isDefinedAt`; `collect` takes a partial function (`List(1, 2, 3).collect({ case i if i % 2 == 1 => i * 2 })` is `List(2, 6)`); partial functions combine with `orElse`, and `applyOrElse(4, _ + 1)` supplies a default.
- A method can be passed where a function is expected (eta-expansion).
- A by-name parameter is written `body: => Unit` and is not evaluated at the call; it is evaluated on demand, which is how custom control structures are written.
Verify: `List(1, 2, 3).collect(pf)` returns only the elements pf is defined for.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 book pages Partial Functions, Eta-Expansion and Control Structures. Removed as not confirmed: `lift`, the Scala 2 `_` currying note, the claim that using clauses are a separate parameter list, 'evaluated on each use' wording.

Method: documentation only; no commands were run.
