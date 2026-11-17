---
id: computing-software.software-engineering.scala.sc-validated-error-accumulation
name: sc-validated-error-accumulation
category: computing-software
field: software-engineering
product: scala
tags: [scala, validated-error-accumulation]
level: advanced
status: draft
description: "Collect all validation failures in Scala using Either with a list of errors, or Cats Validated with mapN."
sources: ["https://docs.scala-lang.org/scala3/book/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Error accumulation
- `Either` short-circuits on the first Left in a for-comprehension.
- Cats `ValidatedNel[E, A]` accumulates: `(v1, v2, v3).mapN(User.apply)` returns `Valid` or `Invalid(NonEmptyList(...))` (confirm Cats version for imports `cats.syntax.all.*`).
- Convert with `.toEither` / `.toValidated` when mixing styles.
Verify: feed two invalid fields and see both errors reported.
