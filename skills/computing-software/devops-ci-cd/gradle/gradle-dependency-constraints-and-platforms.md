---
id: computing-software.devops-ci-cd.gradle.gradle-dependency-constraints-and-platforms
name: gradle-dependency-constraints-and-platforms
category: computing-software
field: devops-ci-cd
product: gradle
tags: [dependency-constraints, strictly, platform, bom, java-platform, rich-versions]
level: advanced
status: docs-checked
description: "Control versions with constraints, rich versions and platforms, including how strictly declarations compete."
sources: ["https://docs.gradle.org/current/userguide/dependency_constraints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle dependency constraints and platforms

Declare a dependency without a version and set it in `constraints`, documenting why with `because`:

```kotlin
dependencies {
    implementation("com.fasterxml.jackson.core:jackson-databind")
    constraints {
        implementation("com.fasterxml.jackson.core:jackson-databind:2.16.1") {
            because("tested with this version")
        }
    }
}
```

A constraint can raise a transitive dependency's version (for example `commons-codec:1.15` over the `1.11` that httpclient pulls in) and does nothing if the module is not on the graph. Constraints are themselves transitive: a library's constraints affect its consumers.

By default a constraint means at least this version. Rich versions (`version { strictly("33.1.0-jre") }`) add `strictly` (pin an exact version or range), `prefer` and `reject`. Competing `strictly` declarations at the same depth are intersected and the highest version in the overlap wins; disjoint ranges fail resolution. At different depths the declaration closest to the root wins and deeper ones are dropped. `resolutionStrategy.force(...)` and resolve rules can override `strictly`.

Platforms: publish with the `java-platform` plugin and `constraints { api("...:...:version") }`; consume with `implementation(platform(project(":platform")))` and then omit versions. A `strictly` constraint in a platform is endorsed by default; call `doNotEndorseStrictVersions()` to disable.

Constraints are published only in Gradle Module Metadata, so Maven or Ivy consumers may lose them.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
