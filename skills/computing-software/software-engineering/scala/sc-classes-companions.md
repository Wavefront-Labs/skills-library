---
id: computing-software.software-engineering.scala.sc-classes-companions
name: sc-classes-companions
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-classes, classes-companions]
level: practitioner
status: draft
description: "Define classes with constructor parameters, companion objects, apply methods and private constructors."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Classes, objects and companion objects
- `class P(val name: String, var age: Int)` makes public fields; without `val` a parameter is private to the class.
- `object P { def apply(n: String) = new P(n, 0) }` lets you call `P("x")`; Scala 3 creator applications allow `P("x")` without `new` for classes too.
- A companion object shares private members with its class; `private constructor`: `class P private (...)`.
- `object` is a lazily created singleton; extend `App` or use `@main def run(): Unit` for entry points.
Verify: instantiate with and without `new` in `scala-cli repl`.
