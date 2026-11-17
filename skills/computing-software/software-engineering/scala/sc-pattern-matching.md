---
id: computing-software.software-engineering.scala.sc-pattern-matching
name: sc-pattern-matching
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-case-classes, pattern-matching]
level: practitioner
status: gated
description: "Write patterns with alternatives, guards, binders, typed patterns and custom unapply extractors."
sources: ["https://docs.scala-lang.org/tour/pattern-matching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# match expressions, guards and extractors
- `x match { case 0 | 1 => ...; case n if n > 10 => ...; case s: String => ...; case List(a, b, _*) => ...; case p @ Person(_, 3) => ... }`. (gated: unconfirmed, source is paywalled or blocked)
- A lower-case identifier in a pattern binds; use backticks to match a stable value: ``case `expected` =>``.
- Custom extractor: `object Even { def unapply(n: Int): Boolean = n % 2 == 0 }`.
- Type patterns on generics are erased: `case l: List[String]` is unchecked.
- A non-matching input throws `MatchError`.
Verify: add a final `case _` only when truly needed; otherwise rely on exhaustivity warnings.

## Checked

Date: 2026-11-02. Gated: guards, type patterns, @, unapply and sealed exhaustivity confirmed in the Tour; `|` alternatives, backtick stable identifiers, MatchError and erasure were not on the page.

Method: documentation only; no commands were run.
