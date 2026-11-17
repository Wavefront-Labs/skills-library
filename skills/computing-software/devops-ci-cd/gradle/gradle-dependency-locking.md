---
id: computing-software.devops-ci-cd.gradle.gradle-dependency-locking
name: gradle-dependency-locking
category: computing-software
field: devops-ci-cd
product: gradle
tags: [dependency-locking, gradle-lockfile, write-locks, update-locks, lock-mode]
level: advanced
status: docs-checked
description: "Pin dynamic dependency versions with Gradle lock state, update it selectively and choose strict or lenient lock modes."
sources: ["https://docs.gradle.org/current/userguide/dependency_locking.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle dependency locking

Enable locking per configuration with `resolutionStrategy.activateDependencyLocking()`, or for all project configurations with `dependencyLocking { lockAllConfigurations() }` (buildscript configurations are not included).

Write or refresh lock state:

```bash
./gradlew dependencies --write-locks
./gradlew dependencies --update-locks org.apache.commons:commons-lang3,org.slf4j:slf4j-api
```

`--write-locks` creates or overwrites lock state for each resolved configuration; nothing is written if the build fails. `--update-locks` takes comma-separated `group:name` modules and supports wildcards such as `org.apache.commons:*` or `*:guava`.

Each project stores lock state in `gradle.lockfile` at its root; the buildscript lockfile is `buildscript-gradle.lockfile`. Check lockfiles into source control. Customise with:

```kotlin
dependencyLocking {
    lockFile = file("$projectDir/locking/gradle-${scalaVersion}.lockfile")
}
```

Ignore dependencies with `ignoredDependencies.add("com.example:*")` (`<group>:<name>` with optional trailing `*`; `*:*` is rejected). Ignored dependencies are omitted when writing, but their transitives remain locked.

Lock modes:
- Default: resolution must match the lock state.
- `STRICT`: also fails if a locked configuration has no lock state.
- `LENIENT`: still pins dynamic versions but allows added or removed dependencies and shifting transitive versions.

```kotlin
dependencyLocking { lockMode = LockMode.STRICT }
```

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
