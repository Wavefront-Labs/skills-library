---
id: computing-software.software-engineering.scala.sc-val-var-expressions
name: sc-val-var-expressions
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-basics, val-var-expressions]
level: intro
status: docs-checked
description: "Prefer val, use lazy val deliberately, and use if, match and blocks as expressions."
sources: ["https://docs.scala-lang.org/tutorials/FAQ/initialization-order.html", "https://docs.scala-lang.org/scala3/book/control-structures.html", "https://docs.scala-lang.org/scala3/reference/changed-features/lazy-vals-init.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# val, lazy val and expressions
- A strict (eager) `val` is one that is not a `lazy val`; strict vals are set during construction, so a `lazy val` is the way to delay initialisation.
- If a lazy val's right-hand side throws, it is re-evaluated on the next access; cycles among lazy vals can overflow the stack, and thread-safe lazy vals in Scala 3 risk deadlock (recursive lazy vals are undefined).
- When every construct returns a value the style is called expression-oriented programming (see Control Structures).
Verify: evaluate each form in the REPL.

## Checked

Date: 2026-11-02. Confirmed on the Scala FAQ page on initialization order, the Scala 3 book page Control Structures and the Scala 3 reference page Lazy Vals Initialization. Removed as not confirmed: `val`/`var` mutability text, 'evaluates once with a lock' detail, indentation and `end` marker remarks, explicit-annotation advice.

Method: documentation only; no commands were run.
