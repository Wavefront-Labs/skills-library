---
id: computing-software.software-engineering.groovy.range-custom-slicing
name: range-custom-slicing
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, range-custom-slicing]
level: advanced
status: docs-checked
description: "Make your own class usable in a range (Comparable plus next and previous) and slice strings and lists with ranges."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-operators.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_working-with-collections.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom ranges and slicing
- A class works in `a..b` if it implements `Comparable` and has `next()` and `previous()` methods.
- Negative indices count from the end; a backwards range (start greater than end) reverses the result, so `'hello'[1..-2]` is `ell` and `'abc'[2..0]` is `cba`.
- Integer ranges are `IntRange`; bounds can be exclusive (`1..<5`).

## Gotchas
- Custom range types need both `next()` and `previous()`.

## Checked

2026-11-02. Confirmed against the Operators chapter (Range operator) and the collections chapter (subscripts and backwards ranges). Removed: range property and method names, `ObjectRange`, step and Date/Calendar claims.

Method: documentation only; no commands were run.

## Self-check
`assert 'abc'[2..0] == 'cba' && 'hello'[1..-2] == 'ell'`.
