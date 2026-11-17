---
id: computing-software.software-engineering.kotlin.kt-string-templates
name: kt-string-templates
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-strings, string-templates]
level: intro
status: docs-checked
description: "Format text with templates, raw strings, trimIndent and buildString."
sources: ["https://kotlinlang.org/docs/strings.html", "https://kotlinlang.org/docs/coding-conventions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String templates raw strings and buildString
- String templates insert values with `$name` or an expression in braces such as `${text.length}`.
- Raw strings use triple quotes; clean indentation with `trimIndent()` (no internal indentation needed) or `trimMargin()` (internal indentation kept).
- Build strings in loops with `buildString { }` or `StringBuilder`.
Verify: print the result for multi-line input and check the indentation.

## Checked
2026-11-03. Confirmed on the Kotlin strings page and coding conventions page: templates, raw strings, trimIndent/trimMargin, buildString.
Removed: the `${'$'}` escape, `joinToString` prefix/postfix parameters, and `"%.2f".format` with `Locale.ROOT` (not on the pages).
Method: documentation only; no commands were run.
