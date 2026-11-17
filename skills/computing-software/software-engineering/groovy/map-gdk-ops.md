---
id: computing-software.software-engineering.groovy.map-gdk-ops
name: map-gdk-ops
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, map-gdk-ops]
level: practitioner
status: docs-checked
description: "Iterate and transform maps with the GDK: each with an entry or key and value, findAll returning a Map, collectEntries, subMap and sort."
sources:
  - https://github.com/apache/groovy/blob/master/src/main/java/org/codehaus/groovy/runtime/DefaultGroovyMethods.java
  - https://groovy-lang.org/groovy-dev-kit.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map GDK iteration and transformation
These methods are defined for `Map` in `DefaultGroovyMethods`:
- `each(Map, Closure)` and `eachWithIndex(Map, Closure)` take a closure that accepts either a single `Map.Entry` or a key and a value (the closure parameters are declared as `MapEntryOrKeyValue`).
- `findAll(Map, Closure)` returns a `Map` of the matching entries; there is also a `BiPredicate` overload.
- `collectEntries` builds a new `Map` from the results of a closure; `subMap` and `sort(Map)` exist as well.

## Checked

2026-11-03. Confirmed against the `DefaultGroovyMethods` source (signatures of `each`, `eachWithIndex`, `findAll`, `collectEntries`, `subMap`, `sort` for maps). Removed: code snippets with asserted results, `groupBy`, `count`, the `+` operator claim and the `collect` return-type note.

Method: documentation only; no commands were run.
