---
id: computing-software.software-engineering.groovy.bigdecimal-default
name: bigdecimal-default
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, bigdecimal-default, groovy-numbers]
level: practitioner
status: docs-checked
description: "Groovy decimal literals are BigDecimal, integer division yields BigDecimal, and arithmetic promotion rules."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_working-with-numbers.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-differences-java.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigDecimal default and number promotion
- `1.1` is `BigDecimal`; use `1.1d`/`1.1f` for double/float. With `def`, an integral literal takes the type that can hold it.
- `/` on two integral operands returns `BigDecimal` (non-exact results use a scale of at least 10); use `intdiv()` for integer division.
- `**` is power: `2**10 == 1024`.
- `int` with `int` gives `int` in the result-type table; declare `long`/`BigInteger` early when values can grow.
- BigDecimal division scale and precision rules are in the Working with numbers chapter.

## Gotchas
- `==` uses `compareTo` for Comparable types such as `BigDecimal`.

## Self-check
`assert 7.intdiv(2) == 3 && (1/3) instanceof BigDecimal`.

## Checked

2026-11-02. Confirmed against Working with numbers (decimal literals, result-type table, division, power) and Differences from Java (== behaviour). Removed: the 0.1+0.2 and 1.0.equals(1.00) claims, the 0.3333333333 figure and the remainder wording.

Method: documentation only; no commands were run.
