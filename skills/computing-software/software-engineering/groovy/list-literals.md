---
id: computing-software.software-engineering.groovy.list-literals
name: list-literals
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, list-literals, groovy-lists]
level: intro
status: docs-checked
description: "Create and index Groovy lists: literals, negative indexes, slices, left-shift append, and typed arrays."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-syntax.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_working-with-collections.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List literals and indexing
- `def l = [1, 2, 3]` is a `java.util.ArrayList`; `[] as LinkedList` or `new LinkedList(l)` for others.
- Index: `l[0]`, `l[-1]` (last), `l[1..2]` (slice), `l[0, 2]` (selected).
- Append with `l << 4`.
- Arrays: `int[] a = [1, 2]` or `[1, 2] as int[]`.

## Gotchas
- `l - 2` removes by value, not index; use `l.remove(0)` for index.
- `remove(int)` removes by index and `remove(Object)` by value; on a list of integers use `removeAt` for an index and `removeElement` for a value.

## Self-check
`assert [1,2,3][-1] == 3`.

## Checked

2026-11-02. Confirmed against the Syntax chapter (lists, arrays) and Working with collections (remove, removeAt, removeElement, minus). Removed: out-of-range read and write behaviour, `+=` and `add`, asImmutable.

Method: documentation only; no commands were run.
