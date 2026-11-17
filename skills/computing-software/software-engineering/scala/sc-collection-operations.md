---
id: computing-software.software-engineering.scala.sc-collection-operations
name: sc-collection-operations
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-collections, collection-operations]
level: practitioner
status: draft
description: "Transform collections with higher-order methods and avoid intermediate allocations with views and iterators."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# map, flatMap, fold, groupBy and views
- `map`, `flatMap`, `filter`, `collect { case ... }`, `foldLeft(0)(_ + _)`, `groupBy`, `groupMap(k)(v)`, `partition`, `zipWithIndex`, `sliding`, `grouped`.
- `reduce` throws on empty input; `reduceOption` or `foldLeft` do not.
- `.view` makes operations lazy; `.iterator` for single pass; `LazyList` is lazy and memoising.
- `groupMapReduce(key)(value)(combine)` replaces groupBy plus map.
- `toMap` on duplicate keys keeps the last; `sorted`, `sortBy`, `sortWith` are stable.
Verify: compare against a hand-computed result for small input.
