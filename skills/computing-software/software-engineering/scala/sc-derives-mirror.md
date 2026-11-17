---
id: computing-software.software-engineering.scala.sc-derives-mirror
name: sc-derives-mirror
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-derivation, derives-mirror]
level: advanced
status: docs-checked
description: "Derive type class instances for ADTs with derives and the Mirror machinery."
sources: ["https://docs.scala-lang.org/scala3/reference/contextual/derivation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# derives clauses and Mirror
- `case class P(x: Int) derives Show` needs `Show.derived`; the derived instance is created in the companion of the deriving type.
- `derived` takes a `Mirror.Of[T]`; the mirror's `MirroredElemTypes` and `MirroredElemLabels` type members describe the element types and names.
- The reference builds per-field instances with inline methods and `summonInline`.
Verify: derive for a sealed trait and a case class.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 reference page Type Class Derivation. Removed as not confirmed: `derives CanEqual` example wording and the library list (circe, upickle, zio-json, tapir).

Method: documentation only; no commands were run.
