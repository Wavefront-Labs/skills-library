---
id: computing-software.software-engineering.scala.sc-mutable-collections-builders
name: sc-mutable-collections-builders
category: computing-software
field: software-engineering
product: scala
tags: [scala, mutable-collections-builders]
level: practitioner
status: draft
description: "Use scala.collection.mutable (ArrayBuffer, HashMap) and builders deliberately, and convert back to immutable."
sources: ["https://docs.scala-lang.org/scala3/book/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mutable collections
- Import explicitly: `import scala.collection.mutable`; `ArrayBuffer` for append, `ListBuffer` for list building, `mutable.HashMap` with `getOrElseUpdate`.
- `Vector.newBuilder[Int]` / `xs.to(Vector)` for efficient construction; `.toList` or `.toMap` copy out.
- Do not expose mutable collections in public APIs; return immutable views.
Verify: mutate inside a function and return `buf.toList`.
