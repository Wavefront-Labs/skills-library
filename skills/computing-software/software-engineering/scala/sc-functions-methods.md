---
id: computing-software.software-engineering.scala.sc-functions-methods
name: sc-functions-methods
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-functions, functions-methods]
level: practitioner
status: docs-checked
description: "Distinguish def and Function types, use currying, partial application and by-name parameters."
sources: ["https://docs.scala-lang.org/scala3/book/fun-eta-expansion.html", "https://docs.scala-lang.org/scala3/book/control-structures.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Methods versus function values and by-name parameters
- A method can be passed where a function value is expected (eta-expansion), for example to `map`.
- A by-name parameter `body: => Unit` is not evaluated when the method is called; the block runs on demand.
Verify: count evaluations of a by-name argument with a side effect.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 book pages Eta-Expansion and Control Structures. Removed as not confirmed: automatic eta-expansion version claims, the foldLeft multi-parameter-list remark, varargs `xs*` syntax, the extension example.

Method: documentation only; no commands were run.
