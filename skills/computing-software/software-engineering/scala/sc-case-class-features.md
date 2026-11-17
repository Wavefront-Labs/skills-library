---
id: computing-software.software-engineering.scala.sc-case-class-features
name: sc-case-class-features
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-case-classes, case-class-features]
level: practitioner
status: gated
description: "Use equals, hashCode, copy, unapply and the limits of case class inheritance."
sources: ["https://docs.scala-lang.org/tour/case-classes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Case class generated members and copy
- Case classes generate `apply`, `unapply`, `copy`, `equals`, `hashCode`, `toString`, and are `Product` and `Serializable`. (gated: unconfirmed, source is paywalled or blocked)
- `p.copy(age = 3)` makes a modified copy; keep case classes immutable, use `val` fields only.
- Do not extend a case class with another case class; `final case class` is conventional.
- Only fields in the first parameter list take part in equality.
- Arrays in case classes compare by reference.
Verify: `P("a", 1) == P("a", 1)` is true.

## Checked

Date: 2026-11-02. Gated: only apply, copy and structural equality were confirmed in the Tour of Scala; unapply, Product/Serializable, inheritance rule and array equality were not on the page.

Method: documentation only; no commands were run.
