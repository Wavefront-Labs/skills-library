---
id: computing-software.software-engineering.scala.sc-for-comprehensions
name: sc-for-comprehensions
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-for-comprehensions, for-comprehensions]
level: practitioner
status: docs-checked
description: "Use for comprehensions over Option, Either, Future and collections and know how they desugar."
sources: ["https://docs.scala-lang.org/tour/for-comprehensions.html", "https://docs.scala-lang.org/tutorials/FAQ/index.html", "https://docs.scala-lang.org/scala3/reference/changed-features/pattern-bindings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for/yield desugaring and monadic composition
- A `for` expression is syntactic sugar for nested `map`, `flatMap` and `withFilter` calls.
- Comprehensions are not restricted to lists: any datatype that supports `withFilter`, `map` and `flatMap` with the proper types works.
- Pattern bindings in `for` expressions are type-checked more strictly in Scala 3: a refutable pattern such as `for (x, y) <- elems yield (y, x)` on a `List[Any]` is reported at compile time (warning in 3.2+, error under `-source:future`).
Verify: rewrite a comprehension by hand with `flatMap`/`map` and compare results.

## Checked

Date: 2026-11-02. Confirmed on the Tour of Scala For Comprehensions page, the Scala FAQ, and the Scala 3 reference page Pattern Bindings. Removed as not confirmed: the foreach desugaring remark, same-monad mixing rule, Future sequencing advice, `-Xprint:typer`.

Method: documentation only; no commands were run.
