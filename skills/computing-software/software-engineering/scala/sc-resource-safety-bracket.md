---
id: computing-software.software-engineering.scala.sc-resource-safety-bracket
name: sc-resource-safety-bracket
category: computing-software
field: software-engineering
product: scala
tags: [scala, resource-safety-bracket]
level: advanced
status: draft
description: "Acquire and release resources safely in effect systems: cats-effect Resource, ZIO scoped, and Using in the stdlib."
sources: ["https://docs.scala-lang.org/scala3/book/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resource safety
- stdlib: `scala.util.Using(new FileInputStream(f)) { in => ... }` returns a `Try` and closes on exit.
- cats-effect: `Resource.make(acquire)(release).use(r => ...)`; releases on error and cancellation.
- ZIO: `ZIO.acquireRelease` with `ZIO.scoped` (confirm ZIO 2 API).
Verify: throw inside `use` and confirm release ran.
