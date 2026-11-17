---
id: computing-software.software-engineering.kotlin.kt-preconditions
name: kt-preconditions
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-errors, preconditions]
level: intro
status: docs-checked
description: "Validate with require, check, error and checkNotNull and choose exception types intentionally."
sources: ["https://kotlinlang.org/docs/exceptions.html", "https://kotlinlang.org/docs/java-to-kotlin-interop.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions and preconditions
- `require(cond) { msg }` throws IllegalArgumentException (input validity); `check(cond)` and `error(msg)` throw IllegalStateException (state).
- Kotlin treats all exceptions as unchecked; for Java callers a Java checked exception must be declared with `@Throws`.
Verify: unit tests assert the exception class and message.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (exceptions.html, java-to-kotlin-interop.html): require/check/error exceptions, unchecked exceptions; @Throws is covered by Java-to-Kotlin interop. Removed as not stated there: checkNotNull/requireNotNull smart-cast, TODO() and the Swift interop remark (not read).

Method: documentation only; no commands were run.
