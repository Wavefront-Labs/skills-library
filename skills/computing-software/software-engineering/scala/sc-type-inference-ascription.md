---
id: computing-software.software-engineering.scala.sc-type-inference-ascription
name: sc-type-inference-ascription
category: computing-software
field: software-engineering
product: scala
tags: [scala, type-inference-ascription]
level: practitioner
status: docs-checked
description: "Know how Scala infers types, when to annotate public members, and the Any/AnyVal/AnyRef/Nothing/Null hierarchy."
sources: ["https://docs.scala-lang.org/scala3/reference/new-types/union-types.html", "https://docs.scala-lang.org/scala3/guides/migration/incompat-contextual-abstractions.html", "https://docs.scala-lang.org/scala3/guides/migration/incompat-type-inference.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type inference
- Annotate the result types of implicit and given definitions: the Scalafix rule `ExplicitResultTypes` can write missing result-type annotations when migrating to Scala 3.
- A union type is inferred for an expression only when written explicitly (or when the common supertype is transparent); `if (c) 1 else "a"` is widened to the common supertype rather than `Int | String`.
- The explicit-nulls mode is enabled with `-Yexplicit-nulls` (disabled by default).
Verify: inspect inferred types in the REPL or IDE hover.

## Checked

Date: 2026-11-02. Confirmed on Union Types reference (no inference of unions unless explicit), the migration pages for contextual abstractions and type inference (ExplicitResultTypes), and the explicit-nulls internals page (flag name, off by default). Fixed: the skill claimed `if (c) 1 else "a"` infers `Int | String` in Scala 3, the reference says it does not. Removed as not confirmed: bottom-type remarks, `List(1, 2.0)` widening, compile-time and binary-compatibility rationale, `:type` REPL command, ascription.

Method: documentation only; no commands were run.
