---
id: computing-software.software-engineering.scala.sc-property-based-testing
name: sc-property-based-testing
category: computing-software
field: software-engineering
product: scala
tags: [scala, property-based-testing]
level: advanced
status: draft
description: "Write ScalaCheck properties, generators and shrinking, integrated with munit-scalacheck or ScalaTest."
sources: ["https://docs.scala-lang.org/scala3/book/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ScalaCheck
- `forAll { (xs: List[Int]) => xs.reverse.reverse == xs }`; custom `Gen` via `Gen.oneOf`, `Gen.listOf`, for-comprehensions; `Arbitrary` instances for your types.
- Failures are shrunk to a minimal counterexample; set `minSuccessfulTests` and the seed to replay.
- Use with munit (`ScalaCheckSuite`) or ScalaTest `ScalaCheckPropertyChecks`.
Verify: a deliberately wrong property reports a shrunken case.
