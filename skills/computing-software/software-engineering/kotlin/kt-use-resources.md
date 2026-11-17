---
id: computing-software.software-engineering.kotlin.kt-use-resources
name: kt-use-resources
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-errors, use-resources]
level: practitioner
status: docs-checked
description: "Close Closeable and AutoCloseable resources with use and handle suppressed exceptions."
sources: ["https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.io/use.html", "https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/use.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource management with use
- `resource.use { ... }` executes the block and closes the resource whether the block completes normally or throws. There are versions for `Closeable` (kotlin.io) and `AutoCloseable` (kotlin).
- If both the block and `close()` throw, the exception from `close` is added to the primary exception as a suppressed exception.
Verify: test that `close()` is called when the block throws.

## Checked
2026-11-03. Confirmed on the `use` API pages for Closeable and AutoCloseable: closing on normal and exceptional exit, suppressed exceptions.
Removed: the `bufferedReader().use { readText() }` example and the advice not to return a resource out of `use` (not on the pages).
Method: documentation only; no commands were run.
