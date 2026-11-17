---
id: computing-software.software-engineering.scala.sc-derives-clause-mirror
name: sc-derives-clause-mirror
category: computing-software
field: software-engineering
product: scala
tags: [scala, derives-clause-mirror]
level: sme
status: docs-checked
description: "Use the Scala 3 derives clause with Mirror, tuple-based derivation, and when to prefer libraries (circe, upickle)."
sources: ["https://docs.scala-lang.org/scala3/reference/contextual/derivation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# derives
- For `DerivingType derives TC`, a derived instance is created in the companion object of `DerivingType` using `TC.derived`; you can also call `derived` manually when you do not control the type, though a `derives` clause is preferred.
- `derived` takes a `Mirror.Of[T]`; the mirror type members include `MirroredElemTypes` and `MirroredElemLabels`.
- The reference implements `derived` with inline methods, inline matches and `summonInline` to collect the instances for the element types.
Verify: derive for a case class and an enum and use the instance.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 reference page Type Class Derivation. Removed as not confirmed: library names and versions (circe, upickle), the `summonAll` remark, 'product uses MirroredElemTypes, sum uses labels' split.

Method: documentation only; no commands were run.
