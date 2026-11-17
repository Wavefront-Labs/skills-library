---
id: computing-software.software-engineering.kotlin.kt-collection-operations
name: kt-collection-operations
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-collections, collection-operations]
level: practitioner
status: docs-checked
description: "Use groupBy, associate, partition, fold and zip instead of manual loops."
sources: ["https://kotlinlang.org/docs/collection-grouping.html", "https://kotlinlang.org/docs/collection-aggregate.html", "https://kotlinlang.org/docs/collection-transformations.html", "https://kotlinlang.org/docs/collection-parts.html", "https://kotlinlang.org/docs/collection-filtering.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grouping, associating and aggregating
- `groupBy { it.type }` returns a Map of key to list of elements; `associateBy { it.id }` returns a Map where, if two elements share a key, only the last one remains; `partition { }` returns a Pair of lists.
- `fold(init) { acc, x -> }` takes an initial value; every `reduce` operation throws on an empty collection. `maxOf`/`minOf` throw `NoSuchElementException` on empty input, while `maxByOrNull`/`...OrNull` variants return null.
- Also available: `sumOf { }`, `zip`, `windowed`, `chunked` (`windowed` overlaps by default step 1, so `[1, 2, 3, 4]` gives `[[1, 2], [2, 3], [3, 4]]`).
- `groupingBy { }.eachCount()` counts per key without building lists.
Verify: tests with empty input prove the reduce/max choices.

## Checked
2026-11-03. Confirmed on the collection grouping, aggregate, transformations, parts and filtering pages: groupBy, groupingBy/eachCount, associateBy last-wins, partition, fold/reduce on empty collections, OrNull variants, maxOf/minOf exceptions, sumOf, zip, windowed vs chunked.
Removed: nothing beyond tightening wording.
Method: documentation only; no commands were run.
