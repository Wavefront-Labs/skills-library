---
id: computing-software.software-engineering.scala.sc-exceptions-resources
name: sc-exceptions-resources
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-options-errors, exceptions-resources]
level: practitioner
status: draft
description: "Use try/finally and scala.util.Using to close resources safely."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exceptions and resource management
- `try ... catch { case e: IOException => ... } finally { ... }` is an expression.
- `Using(new FileReader(f)) { r => ... }` (2.13 and Scala 3) closes resources and returns a `Try`; `Using.Manager` for several resources.
- `throw` has type `Nothing`; Scala has no checked exceptions; document with `@throws`.
- Avoid using exceptions for control flow; `scala.util.boundary` and `break` is the Scala 3.3 mechanism for non-local returns.
Verify: assert the resource closes when the body throws.
