---
id: computing-software.software-engineering.scala.sc-numeric-string-types
name: sc-numeric-string-types
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-basics, numeric-string-types]
level: intro
status: draft
description: "Handle Int overflow, BigDecimal, string interpolators and multiline strings."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Numeric types, strings and interpolation
- `Int` wraps on overflow; use `Math.addExact` to throw or `BigInt`/`BigDecimal` (construct from strings, `BigDecimal("0.1")`).
- Interpolators: `s"x=$x ${a + b}"`, `f"$x%.2f"`, `raw"\n"`.
- Triple-quoted strings with `.stripMargin`.
- `==` is structural equality (null-safe), `eq` is reference equality.
- `1 / 2` is `0`; write `1.0 / 2`.
Verify: print `Int.MaxValue + 1`.
