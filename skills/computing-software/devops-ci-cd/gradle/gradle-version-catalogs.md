---
id: computing-software.devops-ci-cd.gradle.gradle-version-catalogs
name: gradle-version-catalogs
category: computing-software
field: devops-ci-cd
product: gradle
tags: [version-catalog, libs-versions-toml, bundles, plugin-alias, version-ref, shared-catalog]
level: practitioner
status: docs-checked
description: "Declare dependencies and plugins in libs.versions.toml, understand generated accessors and share or publish catalogs."
sources: ["https://docs.gradle.org/current/userguide/version_catalogs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle version catalogs

`gradle/libs.versions.toml` is imported automatically as the `libs` catalog.

```toml
[versions]
groovy = "3.0.5"
my-lib = { strictly = "[1.0, 2.0[", prefer = "1.2" }

[libraries]
groovy-core = { module = "org.codehaus.groovy:groovy", version.ref = "groovy" }
groovy-json = { group = "org.codehaus.groovy", name = "groovy-json", version = "3.0.5" }
my-lib-short = "com.mycompany:mylib:1.4"

[bundles]
groovy = ["groovy-core", "groovy-json"]

[plugins]
versions = { id = "com.github.ben-manes.versions", version = "0.45.0" }
```

A version table may hold `require`, `strictly`, `prefer`, `reject` or `rejectAll`. Catalogs declare requested versions only; conflict resolution and platforms can still select others.

Accessors: dashes and underscores become dots (`ktor-client-core` becomes `libs.ktor.client.core`); camelCase avoids subgroups; aliases cannot start with `bundles`, `versions` or `plugins`. Use `libs.versions.jackson.asProvider()` if a subgroup blocks a parent version.

Usage: `implementation(libs.groovy.core)`, `implementation(libs.bundles.groovy)`, `alias(libs.plugins.versions)`. Pass the provider, not `.get()`, to APIs such as dependency substitution.

Sharing: publish with the `version-catalog` and `maven-publish` plugins (`catalog { versionCatalog { from(files("gradle/libs.versions.toml")) } }`) and consume with `versionCatalogs { create("libs") { from("com.mycompany:catalog:1.0") } }` in `dependencyResolutionManagement` in settings. Override after import with `version("groovy", "3.0.6")`; call `from()` once per catalog. Extra catalogs get their own accessor (`tools.errorprone.annotations`). TOML files cannot reference each other, and `buildSrc` must import the catalog again in its own settings.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
