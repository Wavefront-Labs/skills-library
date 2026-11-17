---
id: computing-software.software-engineering.kotlin.kt-coding-conventions
name: kt-coding-conventions
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-tooling, coding-conventions]
level: intro
status: docs-checked
description: "Apply the official Kotlin coding conventions for naming, layout and idioms."
sources: ["https://kotlinlang.org/docs/coding-conventions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kotlin coding conventions
- Packages lowercase without underscores; classes and objects upper camel case; functions, properties and locals lower camel case without underscores.
- Constants (`const val`, or top-level/object `val` holding deeply immutable data) use screaming snake case. Enum constants may be either screaming snake case or upper camel case.
- Prefer an expression body for a function whose body is a single expression; use four spaces for indentation, never tabs.
- Trailing commas are encouraged at the declaration site and optional at the call site.
- A file holding one class is named after it; otherwise name it for what the code does and avoid meaningless words such as `Util`.
- Test code (only) may use backticked method names with spaces.

## Checked
2026-11-03. Confirmed against the Kotlin coding conventions page: package, class, function and constant naming, enum constant styles, four-space indent, expression bodies, trailing comma guidance, source file naming, backticked test names.
Removed: "val over var", "explicit return types for public APIs" and the `.editorconfig` KOTLIN_OFFICIAL line (not on the page).
Method: documentation only; no commands were run.
