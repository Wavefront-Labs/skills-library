---
id: computing-software.software-engineering.java.gradle-version-catalogs-and-convention-plugins
name: gradle-version-catalogs-and-convention-plugins
category: computing-software
field: software-engineering
product: java
tags: [java, java-build, gradle, version-catalogs, convention-plugins, build-logic, multi-project]
level: practitioner
status: docs-checked
description: "Centralise dependency versions with gradle/libs.versions.toml and share build logic with precompiled convention plugins in an included build-logic build."
sources:
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/dependency-management/centralizing-dependencies/version_catalogs.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/plugin-development/implementing_gradle_plugins_precompiled.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/plugin-development/implementing_gradle_plugins_convention.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/structuring-builds/composite_builds.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/structuring-builds/sharing_build_logic_between_subprojects.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradle version catalogs and convention plugins

**Goal:** every subproject uses the same versions and the same build conventions, defined once, without `allprojects {}` blocks.

## 1. Version catalog
```toml
# gradle/libs.versions.toml
[versions]
# replace the placeholders with current releases
junit = "<junit-version>"
jackson = "<jackson-version>"
kotlin = "<kotlin-version>"

[libraries]
jackson-databind = { module = "com.fasterxml.jackson.core:jackson-databind", version.ref = "jackson" }
junit-bom = { module = "org.junit:junit-bom", version.ref = "junit" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter" }

[bundles]
testing = ["junit-jupiter"]

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
```
Use in builds:
```kotlin
plugins { alias(libs.plugins.kotlin.jvm) }
dependencies {
    implementation(libs.jackson.databind)
    testImplementation(platform(libs.junit.bom))
    testImplementation(libs.bundles.testing)
}
```
Dashes in aliases become dots (`jackson-databind` -> `libs.jackson.databind`). Catalogs only declare coordinates; they do not force versions on transitives (use platforms/constraints for that).

## 2. Convention plugins in build-logic
```
settings.gradle.kts          -> pluginManagement { includeBuild("build-logic") }
build-logic/settings.gradle.kts
build-logic/build.gradle.kts -> plugins { `kotlin-dsl` }
build-logic/src/main/kotlin/acme.java-conventions.gradle.kts
```
```kotlin
// build-logic/build.gradle.kts
plugins { `kotlin-dsl` }
repositories { gradlePluginPortal() }
dependencies { implementation("<group>:<artifact>:<version>") }   // external plugins that the convention scripts apply
```
```kotlin
// acme.java-conventions.gradle.kts
plugins { java }
java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }
tasks.withType<Test>().configureEach { useJUnitPlatform(); maxParallelForks = 2 }
```
Subprojects: `plugins { id("acme.java-conventions") }`. To use the main catalog inside build-logic, add this to `build-logic/settings.gradle.kts`: `dependencyResolutionManagement { versionCatalogs { create("libs") { from(files("../gradle/libs.versions.toml")) } } }`. Inside precompiled scripts read it with `extensions.getByType(VersionCatalogsExtension::class.java).named("libs")` and `findLibrary("name").get()`; the `plugins {}` block of a precompiled script cannot use the catalog.

## 3. Updating
- Change one line in `libs.versions.toml` to move every module that uses the alias.
- Catalogs declare requested versions only; they do not enforce them, so conflict resolution still applies.

## Gotchas
- Convention plugins can live in `buildSrc` (simplest, on the build classpath automatically) or in an included build commonly named `build-logic` (more scalable for multi-project builds).
- Plugin dependencies used by convention plugins must be on build-logic's classpath (declared as `implementation` of their marker/artifact), not applied with versions in the precompiled script.

## Verify
- No build script outside the catalog hard-codes a version, and a catalog version bump changes the resolved version in every module (check with `dependencyInsight`).

## Checked

Date: 2026-10-25. Documentation release: Gradle 9.8.2 user guide sources (GitHub master; release of 2026-10-19).

Confirmed: `gradle/libs.versions.toml` is picked up automatically for the main build; catalogs capture coordinates and request but do not enforce versions; alias dash mapping; the precompiled-script catalog access pattern (`VersionCatalogsExtension`, `findLibrary`) and the `plugins {}` limitation; importing a catalog into a nested build via `dependencyResolutionManagement { versionCatalogs { create("libs") { from(files(...)) } } }`; convention plugins preferred over `allprojects {}` / `subprojects {}`; `buildSrc` versus an included `build-logic` build; plugin builds included through `pluginManagement`.

Removed as unconfirmed: Spotless and the ben-manes versions plugin, claims about Renovate/Dependabot, pinned example versions (now placeholders), the `the<LibrariesForLibs>()` workaround and the claim that buildSrc invalidates the whole build.

Method: documentation only; no commands were run.
