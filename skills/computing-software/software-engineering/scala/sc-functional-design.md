---
id: computing-software.software-engineering.scala.sc-functional-design
name: sc-functional-design
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-immutability, functional-design]
level: practitioner
status: draft
description: "Structure code as pure functions over immutable data and push side effects to the edges."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pure functions, immutability and referential transparency
- Use immutable collections and case classes; update with `copy`, `updated`, `+`, `:+`.
- Keep functions total: return `Option`/`Either` instead of throwing or returning null.
- Isolate IO at the boundary (main, handlers); pass data in, return data out.
- Tail recursion: `@tailrec` makes the compiler verify the optimisation; `foldLeft` often replaces loops.
- Use `Iterator` or `LazyList` for large or infinite sequences to avoid holding all elements.
Verify: unit tests need no mocks for pure code.
