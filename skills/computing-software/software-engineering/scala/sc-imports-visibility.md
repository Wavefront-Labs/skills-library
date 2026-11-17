---
id: computing-software.software-engineering.scala.sc-imports-visibility
name: sc-imports-visibility
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-packages, imports-visibility]
level: intro
status: docs-checked
description: "Organise code in packages and use import renaming and private, protected and qualified access."
sources: ["https://docs.scala-lang.org/scala3/reference/changed-features/imports.html", "https://docs.scala-lang.org/scala3/book/domain-modeling-oop.html", "https://docs.scala-lang.org/scala3/book/taste-toplevel-definitions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packages, wildcard imports and access modifiers
- Scala 3 wildcard import is `import scala.annotation.*`; rename with `as` and exclude with `as _`, as in `import Predef.{augmentString as _, *}`. The old `_` wildcard and `=>` renaming are still accepted for cross-building.
- Scala 3 replaces package objects with top-level definitions.
- Members can be `private` or `protected`; protected members are also visible to subclasses.
Verify: compile a file that uses a private member from outside its class.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 reference page Imports and the Scala 3 book (Domain Modeling OOP, Top-Level Definitions). Removed as not confirmed: `private[acme]` package qualification, 'narrower than Java's protected' claim, imports inside methods.

Method: documentation only; no commands were run.
