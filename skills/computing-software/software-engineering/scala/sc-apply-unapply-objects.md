---
id: computing-software.software-engineering.scala.sc-apply-unapply-objects
name: sc-apply-unapply-objects
category: computing-software
field: software-engineering
product: scala
tags: [scala, apply-unapply-objects]
level: practitioner
status: docs-checked
description: "Write companion apply factories and custom unapply extractors, plus object as singleton and entry point."
sources: ["https://docs.scala-lang.org/tour/extractor-objects.html", "https://docs.scala-lang.org/scala3/reference/changed-features/pattern-matching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apply and unapply
- Extractors are objects that expose a method `unapply` or `unapplySeq`; `unapply` is what makes `case Point(x, y)` patterns work.
- `unapplySeq` is for extractors that return an arbitrary number of values, for varargs-style patterns.
Verify: a pattern match on your type compiles.

## Checked

Date: 2026-11-02. Confirmed on the Tour of Scala page Extractor Objects and the Scala 3 reference page Option-less pattern matching (extractor definition). Removed as not confirmed: companion apply and private-constructor factory advice, the `@main` and `App` entry-point lines, the exact `unapply` signature.

Method: documentation only; no commands were run.
