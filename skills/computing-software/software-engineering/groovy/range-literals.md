---
id: computing-software.software-engineering.groovy.range-literals
name: range-literals
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, range-literals, groovy-ranges]
level: intro
status: docs-checked
description: "Inclusive and exclusive ranges, reverse and custom-step ranges, ranges of strings and dates."
sources:
  - https://groovy-lang.org/operators.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-operators.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_working-with-collections.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Range literals and iteration
- `1..5` inclusive, `1..<5` exclusive upper bound, `1<..5` exclusive lower bound, `1<..<5` both exclusive.
- A `groovy.lang.Range` implements `List`, so `size()` works; only the bounds are stored.
- Non-numeric: `'a'..'e'`, and any `Comparable` with `next()` and `previous()` methods.
- Use in slicing (`list[range]`) and in `switch` cases, where a range matches as a collection.

## Gotchas
- Use `0..<list.size()` not `0..list.size()` to avoid index-out-of-range.

## Self-check
`assert (1..<4).toList() == [1,2,3] && 'a'..'c' == ['a','b','c']`.

## Checked

2026-11-02. Confirmed against the Operators chapter (range operator, subscript) and Working with collections (half-open and full-open ranges). Removed: the 5..1 reverse claim, step(), toList()/each/contains, negative-index slice example and the version hedge.

Method: documentation only; no commands were run.
