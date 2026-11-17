---
id: computing-software.software-engineering.kotlin.kt-gradle-kotlin-plugin
name: kt-gradle-kotlin-plugin
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-tooling, gradle-kotlin-plugin]
level: practitioner
status: docs-checked
description: "Configure the Kotlin Gradle plugin, JVM toolchain and compiler options in build.gradle.kts."
sources: ["https://kotlinlang.org/docs/gradle-configure-project.html", "https://kotlinlang.org/docs/gradle-compiler-options.html", "https://kotlinlang.org/docs/java-interop.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradle Kotlin plugin and toolchains
- `kotlin { jvmToolchain(17) }` selects the JDK toolchain for the Kotlin compilation (the configure-project page shows this form).
- Compiler options go in the `compilerOptions` DSL (for example `allWarningsAsErrors` and `freeCompilerArgs`). The older `kotlinOptions {}` block is deprecated since Kotlin 2.0.0; the compiler options page has a migration section.
- `-Xjsr305={strict|warn|ignore}` controls how JSR-305 nullability annotations on Java code are treated.
Verify: run the Gradle build and read the Kotlin Gradle plugin compatibility information for your Gradle version.

## Checked
2026-11-03. Confirmed on the Gradle configure-project, compiler options and Java interop pages: jvmToolchain, compilerOptions with allWarningsAsErrors and freeCompilerArgs, kotlinOptions deprecated from 2.0.0, -Xjsr305 values.
Removed: the version-catalog advice, the `plugins {}` snippet and the Gradle command (not covered by the fetched pages).
Method: documentation only; no commands were run.
