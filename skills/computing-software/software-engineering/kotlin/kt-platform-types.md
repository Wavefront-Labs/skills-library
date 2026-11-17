---
id: computing-software.software-engineering.kotlin.kt-platform-types
name: kt-platform-types
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-null-safety, platform-types]
level: practitioner
status: docs-checked
description: "Treat Java values (T!) safely: declare nullability explicitly and honour nullability annotations."
sources: ["https://kotlinlang.org/docs/java-interop.html", "https://kotlinlang.org/docs/java-to-kotlin-nullability-guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Platform types and Java nullability
- Java declarations without nullability information have platform types written `T!` ("T or T?"); Kotlin issues no compile-time nullability errors for them, and the call can fail at runtime with a null-pointer exception.
- Kotlin reads nullability annotations from JetBrains (`org.jetbrains.annotations`), JSpecify (`org.jspecify.annotations`), Android, JSR-305, FindBugs and Eclipse, and treats them as real types.
- Assign Java results to an explicit type (`val s: String? = javaCall()`) at the boundary.
- The `-Xjsr305={strict|warn|ignore}` compiler flag configures how JSR-305 annotations are checked; see the Java interop page for what each value does.
Verify: an NPE with a Java stack frame at a Kotlin call site usually means an unchecked platform type.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (java-interop.html, java-to-kotlin-nullability-guide.html): T! notation, runtime failure, supported annotation packages, -Xjsr305 option values. Removed as not stated there: androidx.annotation naming (page lists com.android.annotations and android.support.annotations) and the default-strictness remark.

Method: documentation only; no commands were run.
