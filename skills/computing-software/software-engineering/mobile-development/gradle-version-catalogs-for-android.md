---
id: computing-software.software-engineering.mobile-development.gradle-version-catalogs-for-android
name: gradle-version-catalogs-for-android
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, version-catalogs, gradle, libs-versions-toml, dependency-management, agp, bom]
level: practitioner
status: docs-checked
description: "Centralise Android dependencies with Gradle version catalogs: libs.versions.toml sections, accessors, bundles, plugin aliases, platform dependencies and convention-plugin access."
sources: ["https://docs.gradle.org/current/userguide/version_catalogs.html", "https://developer.android.com/build/migrate-to-catalogs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Version catalogs for Android builds

Gradle imports `gradle/libs.versions.toml` automatically as the `libs` catalog; no import code
is needed. Android's guide recommends the default name for the same reason. Do not name a
programmatic catalog `libs` if you already have the default file.

```toml
[versions]
androidGradlePlugin = "<agp-version>"
coroutines = "<version>"

[libraries]
kotlinx-coroutines-android = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-android", version.ref = "coroutines" }
androidx-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "ktx" }

[bundles]
# groups of libraries added together

[plugins]
android-application = { id = "com.android.application", version.ref = "androidGradlePlugin" }
```
- `[versions]`, `[libraries]`, `[bundles]` and `[plugins]` are the sections. A library is
  declared either as `module = "group:name"` or with `group` and `name`; `version.ref` points to
  an entry in `[versions]`.
- Aliases are identifiers separated by a dash or underscore; Gradle generates type-safe
  accessors normalised to dot notation (`android-application` becomes
  `libs.plugins.android.application` for plugins, and library aliases are `libs.<alias>`).
  Dashes create nested accessor groups.
- Plugins are used with `alias(libs.plugins.<name>)` in the `plugins {}` block (with
  `apply false` at the root, as in Android's migration guide).
- Migration steps from Android's guide: create the file in the root project's `gradle` folder,
  add an entry for each dependency in both `[versions]` and `[libraries]`, sync, then replace
  declarations in the build files with catalog names; do the same for plugins.

## In modules
```kotlin
plugins { alias(libs.plugins.android.application) }
dependencies {
    implementation(libs.kotlinx.coroutines.android)
}
```
A Gradle `platform(...)` dependency (for example a BOM) is declared in `dependencies` as
usual; Gradle's page shows `platform("org.junit:junit-bom:5.9.1")`.

## Other catalogs and convention plugins
- Extra catalogs (for example `gradle/tools.versions.toml`) are registered in settings; only
  the `libs.versions.toml` in `gradle/` is automatic.
- Code in `buildSrc` or precompiled script plugins reads the catalog through
  `extensions.getByType(VersionCatalogsExtension)` (Kotlin `the<VersionCatalogsExtension>()`).
- A catalog can also be shared across builds by checking the TOML file into a shared
  repository or publishing it.

## Checked
Confirmed in the Gradle version catalogs page and the Android migration page: default file,
sections, accessor normalisation, plugin aliases, platform dependency example, catalog
extension access and sharing options. Removed as not stated there: the Gradle 7.4 "stable"
claim, the alias prefix clash rule, BOM version-override behaviour, Renovate/Dependabot, and
the `./gradlew` verification commands.
Method: docs-only read of cited pages, 2026-11-08
