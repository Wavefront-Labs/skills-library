---
id: computing-software.software-engineering.scala.sc-traits-mixins
name: sc-traits-mixins
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-classes, traits-mixins]
level: practitioner
status: docs-checked
description: "Compose behaviour with traits and understand initialisation order and linearisation."
sources: ["https://docs.scala-lang.org/scala3/reference/other-new-features/trait-parameters.html", "https://docs.scala-lang.org/tutorials/FAQ/initialization-order.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traits, parameters and initialisation order
- Scala 3 traits can have parameters, like classes: `trait Greeting(val name: String)`.
- Constructors of a superclass run before the subclass sets its fields, so an abstract or overridden `val` can read as `null` (or 0/false) in the superclass constructor.
- Ways to avoid that: use class or trait parameters, or a `lazy val` (abstract `lazy val`s work in Scala 3, not Scala 2). Cycles among lazy vals can overflow the stack on first access.
Verify: print in the constructors of a small hierarchy to see the order.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 reference page Trait Parameters and the Scala FAQ page on initialization order. Removed as not confirmed: linearisation order, `abstract override`, the comma mixin syntax, composition advice.

Method: documentation only; no commands were run.
