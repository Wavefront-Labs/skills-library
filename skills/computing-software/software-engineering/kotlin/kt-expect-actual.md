---
id: computing-software.software-engineering.kotlin.kt-expect-actual
name: kt-expect-actual
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-multiplatform, expect-actual]
level: advanced
status: docs-checked
description: "Share code across targets with expect/actual and structured source sets."
sources: ["https://kotlinlang.org/docs/multiplatform/multiplatform-expect-actual.html", "https://kotlinlang.org/docs/multiplatform/multiplatform-hierarchy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# expect and actual declarations
- The common source set declares an `expect` function; each target provides a matching `actual`. Source sets include `commonMain`, `jvmMain` and `iosMain` (an intermediate set shared by the iOS targets, where the `actual` declarations typically live rather than in the individual platform sets).
- Prefer interfaces plus a factory function or dependency injection over expect/actual where interfaces suffice; the docs recommend that.
- expect/actual classes are in Beta, which produces a warning you can suppress with a compiler option; check the page for your Kotlin version.
Verify: build every target, not just JVM.

## Checked
2026-11-03. Confirmed on the multiplatform expect/actual and hierarchy pages: expect/actual model, iosMain as intermediate source set, interfaces recommended, Beta status of expect/actual classes.
Removed: the `appleMain` source set name (not found on the pages) and the sample function body.
Method: documentation only; no commands were run.
