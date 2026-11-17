---
id: computing-software.software-engineering.swift.swift-collections-hof
name: swift-collections-hof
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-collections-strings, collections-hof]
level: intro
status: draft
description: "Use map, filter, reduce, compactMap and sorted on Swift collections, and know complexity."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Array Dictionary Set and higher-order functions
- `compactMap` drops nils, `flatMap` flattens, `reduce(into:)` avoids copies, `sorted(by:)` returns a new array (sort is introsort-like, not stable by documentation guarantee in older versions; check docs), `Dictionary(grouping:by:)`.
- `lazy` collections defer work; `contains(where:)` and `first(where:)` short-circuit.
- Dictionary access `dict[key, default: 0] += 1`.
Verify: Instruments Time Profiler for hot loops.
