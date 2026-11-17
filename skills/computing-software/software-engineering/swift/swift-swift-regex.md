---
id: computing-software.software-engineering.swift.swift-swift-regex
name: swift-swift-regex
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-collections-strings, swift-regex]
level: advanced
status: draft
description: "Use Swift Regex (5.7+) and RegexBuilder for typed matching."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regex literals and string processing
- `let r = /(\d+)-(\d+)/` literals give typed captures; `try Regex("pattern")` for runtime patterns; `firstMatch(of:)`, `wholeMatch(of:)`, `replacing(_:with:)`.
- RegexBuilder DSL for readable patterns.
- Needs Swift 5.7 toolchain; Apple platforms need OS 13/16-era availability (check availability annotations).
Verify: unit tests for malformed inputs.
