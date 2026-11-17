---
id: computing-software.software-engineering.kotlin.kt-jvm-annotations
name: kt-jvm-annotations
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-java-interop, jvm-annotations]
level: practitioner
status: docs-checked
description: "Expose Kotlin APIs to Java with @JvmStatic, @JvmField, @JvmOverloads, @JvmName and @Throws."
sources: ["https://kotlinlang.org/docs/java-to-kotlin-interop.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling Kotlin from Java annotations
- `@JvmStatic` on a function in an object or companion makes it a real static method for Java callers; `@JvmField` exposes a property as a field; `@JvmOverloads` generates overloads for default parameters; `@file:JvmName("Utils")` renames the generated file class; `@Throws(IOException::class)` lets Java code catch the checked exception.
- Top-level functions compile to static methods in a class named after the file with a `Kt` suffix.
- `@JvmName` is also how to resolve JVM signature clashes between declarations.
Verify: inspect the class with `javap -p`, or write a tiny Java caller in tests.

## Checked
2026-11-03. Confirmed on the "Calling Kotlin from Java" page: @JvmStatic, @JvmOverloads, @Throws, @JvmName and file-class naming with Kt suffix, @JvmName for clashes.
Removed: "erasure" as the stated cause of signature clashes; @JvmField wording kept minimal.
Method: documentation only; no commands were run.
