---
id: computing-software.software-engineering.swift.swift-api-naming
name: swift-api-naming
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-api-design, api-naming]
level: practitioner
status: draft
description: "Name types, methods and labels per the Swift API Design Guidelines."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Naming and argument labels
- Clarity at the point of use; omit needless words; name by role not type.
- Mutating/non-mutating pairs: `sort()`/`sorted()`, `append(_:)`/`appending(_:)`; Boolean properties read as assertions (`isEmpty`); protocols describing capability end in `-able/-ible/-ing`.
- Labels: first argument label omitted only when it forms a grammatical phrase or is an initial-value type conversion.
- UpperCamelCase types, lowerCamelCase everything else; acronyms uniform case (`urlString`, `URL`).
Verify: read call sites aloud.
