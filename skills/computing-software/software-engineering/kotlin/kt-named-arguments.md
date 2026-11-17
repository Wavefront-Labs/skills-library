---
id: computing-software.software-engineering.kotlin.kt-named-arguments
name: kt-named-arguments
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-functions, named-arguments]
level: intro
status: docs-checked
description: "Replace overloads and builders with default and named arguments, and keep calls readable."
sources: ["https://kotlinlang.org/docs/functions.html", "https://kotlinlang.org/docs/java-to-kotlin-interop.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default and named arguments
- Declare `fun connect(host: String, port: Int = 443, tls: Boolean = true)`; call `connect("a", tls = false)`.
- Default values are only evaluated when the function is called without the corresponding argument.
- Named arguments make calls with many parameters (booleans especially) readable.
- Java callers do not see defaults; `@JvmOverloads` (or `@IntroducedAt` for newly added optional parameters) generates overloads.
Verify: change a default and recompile; binary compatibility of public APIs still needs separate care.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (functions.html, java-to-kotlin-interop.html): default values and when they are evaluated, named arguments, @JvmOverloads/@IntroducedAt on the Java-interop page. Removed as not stated there: the Kotlin 1.4 positional-after-named rule and 'defaults may refer to earlier parameters' (not read).

Method: documentation only; no commands were run.
