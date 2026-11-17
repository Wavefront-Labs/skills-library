---
id: computing-software.software-engineering.kotlin.kt-regex
name: kt-regex
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-strings, regex]
level: practitioner
status: docs-checked
description: "Use Regex with matchEntire, find and findAll, and toIntOrNull for safe parsing."
sources: ["https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/-regex/", "https://kotlinlang.org/docs/exceptions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex and string parsing
- Build a `Regex(pattern)` and use `matchEntire(input)` (whole string, returns `MatchResult?`), `find(input)` and `findAll(input)`.
- `toIntOrNull()` returns null instead of throwing `NumberFormatException` on bad input.
Verify: add tests for malformed input.

## Checked
2026-11-03. Confirmed on the kotlin.text.Regex API page (matchEntire, find, findAll, MatchResult?) and the Kotlin exceptions page (toIntOrNull).
Removed: named-group syntax and `groups["y"]` (JVM-only detail not confirmed), `toDoubleOrNull`, `split(limit)`, the advice about caching Regex objects, and the catastrophic-pattern remark.
Method: documentation only; no commands were run.
