---
id: computing-software.software-engineering.scala.sc-inline-macros
name: sc-inline-macros
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-metaprogramming, inline-macros]
level: advanced
status: docs-checked
description: "Use inline methods, compile-time ops and quote/splice macros in Scala 3."
sources: ["https://docs.scala-lang.org/scala3/guides/macros/inline.html", "https://docs.scala-lang.org/scala3/guides/macros/macros.html", "https://docs.scala-lang.org/scala3/guides/macros/compiletime.html", "https://docs.scala-lang.org/scala3/guides/migration/macros.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# inline, quotes and splices
- `inline if` guarantees the branch is chosen at compile time; the compile-time operations guide also covers inline matching and `summonInline`, `summonAll`, `constValue`.
- Macros execute user code at compile time to generate code; the implementation takes `Expr` arguments and a contextual `Quotes`, and cannot be defined and used in the same class/file.
- The Scala 3 compiler cannot expand Scala 2.13 macros, because that API is tied to the 2.13 compiler internals.
Verify: call the inline method with a constant and check the compile-time branch.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 macros guide (Inline, Macros, Compile-time operations) and the migration Macro Libraries page. Removed as not confirmed: the `-Xprint:inlining` flag and the derivation-over-macros advice.

Method: documentation only; no commands were run.
