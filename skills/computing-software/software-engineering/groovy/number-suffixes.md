---
id: computing-software.software-engineering.groovy.number-suffixes
name: number-suffixes
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, number-suffixes]
level: intro
status: docs-checked
description: "Literal suffixes (G, L, I, F, D), underscores, hex, octal and binary literals, and string-to-number conversion."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_working-with-numbers.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Number suffixes and literal forms
- Suffixes: `I` Integer, `L` Long, `G` BigInteger/BigDecimal, `F` Float, `D` Double (case-insensitive: `42g`, `1.5g`).
- Underscores: `1_000_000`. Hex `0xFF`, binary `0b1010`, octal `017`.
- `1e3` is a BigDecimal, not an int.

## Gotchas
- A leading `0` means octal: `010 == 8`.

## Self-check
`assert 0b101 == 5 && 1_000 == 1000 && 1e3 instanceof BigDecimal`.

## Checked

2026-11-02. Confirmed against Working with numbers (suffix table, binary/octal/hex literals, underscores, decimal literals and exponents). Removed: the string-to-number conversion helpers and isInteger() guard.

Method: documentation only; no commands were run.
