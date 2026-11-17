---
id: computing-software.software-engineering.scala.sc-inline-macros-quotes
name: sc-inline-macros-quotes
category: computing-software
field: software-engineering
product: scala
tags: [scala, inline-macros-quotes]
level: sme
status: docs-checked
description: "Write inline methods, quoted code '{...} and splices ${...}, and macro-time checks in Scala 3."
sources: ["https://docs.scala-lang.org/scala3/guides/macros/macros.html", "https://docs.scala-lang.org/scala3/guides/macros/compiletime.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quotes and splices
- A macro is an inline method whose body splices a call to the implementation, e.g. `${ inspectCode('x) }`; the implementation takes `Expr` arguments and a contextual `Quotes`.
- The implementation is executed at compile time, so it must be compiled before it is used: a macro cannot be defined and used in the same class/file, but may share a project when the implementation can be compiled first. Files with calls to not-yet-compiled macros are suspended; `-Xprint-suspension` shows which.
- `Expr[T].valueOrAbort` reads a known value out of an expression; `report.errorAndAbort` reports a compile error.
- `scala.compiletime` has `constValue`, `constValueOpt`, `constValueTuple` and the `summonInline` / `summonAll` family for use in inline methods.
Verify: a bad literal argument produces a compile error.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 macros guide pages (Macros, Compile-time operations). Removed as not confirmed: the separate-module test claim and the preference ordering.

Method: documentation only; no commands were run.
