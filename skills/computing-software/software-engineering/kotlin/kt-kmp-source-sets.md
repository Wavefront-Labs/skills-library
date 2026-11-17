---
id: computing-software.software-engineering.kotlin.kt-kmp-source-sets
name: kt-kmp-source-sets
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-multiplatform, kmp-source-sets]
level: practitioner
status: docs-checked
description: "Configure Kotlin Multiplatform targets and source sets (commonMain, platform sets, intermediate sets) with the default hierarchy template."
sources: ["https://kotlinlang.org/docs/multiplatform/multiplatform-hierarchy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Source sets and targets
A Kotlin Multiplatform module declares targets. The Kotlin Gradle plugin has a built-in default hierarchy template with predefined intermediate source sets (for example `apple`, `ios`, `native`) and creates them automatically from the targets you declare.

```kotlin
// build.gradle.kts of the shared module
kotlin {
    jvm()
    iosArm64(); iosSimulatorArm64()
    sourceSets {
        commonMain.dependencies { /* multiplatform libraries */ }
        iosMain.dependencies { /* iOS-only dependencies */ }
    }
}
```

- The recommended way to set up the hierarchy is the default template; the plugin gives type-safe accessors (`iosMain`, `commonMain`) for its source sets, so you need no `by getting` or `by creating`.
- The toolchain ensures each source set only sees API available on all targets it compiles to. Despite their names, the `apple` and `native` sets compiled only to iOS targets have access to the full iOS API.
- For platform APIs from shared code use expected and actual declarations.
- Sets such as `watchos` are created only when you declare a matching target (for example `watchosArm64`).

Gotchas:
- Manual `dependsOn()` edges cancel the default template and produce the warning "The Default Kotlin Hierarchy Template was not applied". Remove the `dependsOn` calls, or reapply the template with `applyDefaultHierarchyTemplate()` and add extra sets (for example one shared by a JVM and a macOS target) with `dependsOn`.
- Accessing a template source set (for example `linuxX64Main`) without declaring its target gives a warning.
- You cannot modify the template's own `dependsOn` relations; to opt out set `kotlin.mpp.applyDefaultHierarchyTemplate=false` in `gradle.properties` and configure everything manually.
- Sharing one source set across several JVM targets, JVM plus Android, or several JS targets is not supported.

Verify: after declaring targets, check the IDE Project view for the created intermediate source sets and that the build prints no template warning.

## Checked
2026-11-09. Confirmed against the Kotlin Multiplatform "Source set hierarchy" page: default hierarchy template behaviour, type-safe accessors, apple/native full-API note, the dependsOn warning and its fixes, applyDefaultHierarchyTemplate(), the opt-out property, the target-combination limits, expect/actual mention.
Removed: the plugin and library version numbers, the "since Kotlin 1.9.20" claim, the src/<set>/kotlin directory layout, the Gradle test and compile task names, and the claim that an undeclared-target set "silently does nothing" (the page says a warning). The multiplatform-discover-project source was unreadable (stub) and the old hierarchy URL moved to the one listed.
Method: documentation only; no commands were run.
