---
id: computing-software.software-engineering.scala.sc-numeric-math
name: sc-numeric-math
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-numeric-math, numeric-math]
level: practitioner
status: draft
description: "Handle money and precision with BigDecimal, and use scala.math and numeric libraries."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BigDecimal, math functions and numeric libraries
- `BigDecimal("19.99")` from a string is exact; do not construct from a `Double` you intend as exact.
- Set rounding explicitly: `x.setScale(2, BigDecimal.RoundingMode.HALF_EVEN)`.
- `scala.math` wraps `java.lang.Math`; `Math.floorMod` gives a non-negative modulo.
- Breeze and ND4J provide linear algebra; the `Numeric` and `Integral` type classes enable generic numeric code.
Verify: `BigDecimal("0.1") + BigDecimal("0.2") == BigDecimal("0.3")` is true.
