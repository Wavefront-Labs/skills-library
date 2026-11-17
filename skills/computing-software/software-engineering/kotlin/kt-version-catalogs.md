---
id: computing-software.software-engineering.kotlin.kt-version-catalogs
name: kt-version-catalogs
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-tooling, version-catalogs]
level: practitioner
status: docs-checked
description: "Centralise Kotlin and library versions in a Gradle libs.versions.toml version catalog and use it from build.gradle.kts."
sources: ["https://docs.gradle.org/current/userguide/version_catalogs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradle version catalogs
Gradle automatically imports a catalog named `libs.versions.toml` in the `gradle` directory, with no programmatic import needed. Entries are available through the `libs` object.

```toml
# gradle/libs.versions.toml
[versions]
kotlin = "<kotlin-version>"
coroutines = "<coroutines-version>"

[libraries]
coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }

[bundles]
async = ["coroutines-core"]

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
```

```kotlin
// build.gradle.kts
plugins { alias(libs.plugins.kotlin.jvm) }
dependencies { implementation(libs.coroutines.core) }   // or libs.bundles.async
```

- Aliases are identifiers separated by a dash or underscore; type-safe accessors are generated and normalised to dot notation, each dash mapping to a dot (`coroutines-core` becomes `libs.coroutines.core`).
- Use `version.ref` to reference a version from the `[versions]` section so one version drives several libraries.
- In the `plugins {}` block, refer to a catalog plugin with `alias()`; plugins use `libs.plugins.<alias>`.
- Extra catalogs are registered in `settings.gradle.kts` with `versionCatalogs { create("tools") { from(files("gradle/tools.versions.toml")) } }`.
- The catalog can also be shared with `buildSrc` by importing it in `buildSrc/settings.gradle(.kts)` with `from(files("../gradle/libs.versions.toml"))`.

## Checked
2026-11-09. Confirmed against the Gradle "Version catalogs" user guide: automatic import of gradle/libs.versions.toml, the [versions]/[libraries]/[bundles]/[plugins] sections, version.ref, dash-to-dot accessor normalisation, alias() in plugins, the versionCatalogs from(files(...)) registration and the buildSrc import.
Removed: the "stable since Gradle 7.4" claim, the `the<LibrariesForLibs>()` convention-plugin advice, the `./gradlew dependencies` check, and concrete Kotlin and coroutines version numbers (replaced by placeholders). The kotlinlang Gradle page was dropped as a source.
Method: documentation only; no commands were run.
