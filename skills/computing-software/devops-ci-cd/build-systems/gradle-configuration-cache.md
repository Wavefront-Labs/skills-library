---
id: computing-software.devops-ci-cd.build-systems.gradle-configuration-cache
name: gradle-configuration-cache
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, configuration-cache, gradle, gradle-performance, build-scan, isolated-projects, gradle-properties]
level: practitioner
status: docs-checked
description: "Enable and fix the Gradle configuration cache: turn it on, read the problems report, fix incompatible tasks and plugins, CI usage, and how it relates to build cache."
sources: ["https://docs.gradle.org/current/userguide/configuration_cache.html", "https://docs.gradle.org/current/userguide/configuration_cache_enabling.html", "https://docs.gradle.org/current/userguide/configuration_cache_requirements.html", "https://docs.gradle.org/current/userguide/configuration_cache_debugging.html", "https://github.com/gradle/actions/blob/main/docs/setup-gradle.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle configuration cache

The **configuration cache** stores the result of the configuration phase (the task graph with resolved inputs) and reuses it when build scripts, properties and environment inputs are unchanged. It's different from the **build cache**, which reuses task *outputs*. Large builds often spend seconds to minutes configuring before any task runs; the configuration cache removes that work and can also run tasks in parallel.

## Enable
```properties
# gradle.properties
org.gradle.configuration-cache=true
org.gradle.caching=true                          # build cache (separate feature)
org.gradle.parallel=true
```
By default Gradle fails the build when configuration cache problems occur. `org.gradle.configuration-cache.problems=warn` (or `--configuration-cache-problems=warn`) turns problems into warnings, but the documentation advises it only for short-lived troubleshooting. Gradle 9.0 made the configuration cache the preferred mode of execution and the documentation says it will be enabled by default in Gradle 10. A reused entry prints `Reusing configuration cache.`

## Read the problems report
When problems occur, Gradle writes an HTML report at `build/reports/configuration-cache/<hash>/<hash>/configuration-cache-report.html`, grouped by problem and location (plugin or script line).

Typical problems and fixes:
| Problem | Fix |
|---|---|
| `invocation of 'Task.project' at execution time` | capture values at configuration into properties: `val out = layout.buildDirectory`, use injected services |
| reading `System.getenv`/system properties/files at configuration | `providers.environmentVariable("X")`, `providers.gradleProperty`, `providers.fileContents` so they become tracked inputs |
| external process at configuration (`"git rev-parse".execute()`) | `providers.exec { commandLine("git","rev-parse","HEAD") }.standardOutput.asText` |
| task holds a `Project`, `Configuration`, or `Gradle` reference | use `FileCollection`, `Provider`, `ArtifactCollection`; inject `ExecOperations`, `FileSystemOperations` |
| `buildFinished`/`BuildListener` | a build service implementing `OperationCompletionListener`, registered through `BuildEventsListenerRegistry`, or flow actions |
| plugin not compatible | upgrade the plugin and report issues to its maintainers; `notCompatibleWithConfigurationCache("reason")` on the task as a last resort |

## Inputs that invalidate it
Changes to build scripts, `buildSrc`/included builds, `gradle.properties`, and environment variables, system properties and files read through providers. Reading a volatile value (such as a `BUILD_NUMBER` environment variable) at configuration time makes the entry miss on every CI run - read it lazily at execution time.

## CI
- The Gradle documentation lists CI support as "actively evolving". The configuration cache lives in the project and Gradle user home, so it helps CI only when those persist (persistent agents or cached Gradle home with the same checkout path); it is mainly a developer-loop win, while the remote build cache is the CI win.
- Cache entries are encrypted with a key kept in the Gradle user home (or the `GRADLE_ENCRYPTION_KEY` environment variable); anything with the cache directory and the key can read the entries, so restrict access in shared or CI environments. `gradle/actions/setup-gradle` accepts a `cache-encryption-key` input (a base64-encoded AES key) for configuration-cache data stored in the GitHub Actions cache.

## Verify
- [ ] A second identical invocation prints `Reusing configuration cache.` and configuration time is near zero.
- [ ] The problems report is empty on a clean run (the default mode already fails on problems).

## Checked
Date: 2026-10-25. Documentation: Gradle user guide pages "Configuration cache" (overview, enabling, requirements, debugging, adoption) from gradle/gradle `platforms/documentation/docs/src/docs/userguide/optimizing-builds/configuration-cache`, and gradle/actions `docs/setup-gradle.md`.
Confirmed: `org.gradle.configuration-cache` property; problems default to failing the build and the `problems=warn` option with its caveat; `Reusing configuration cache.` message; report location `build/reports/configuration-cache/<hash>/<hash>/configuration-cache-report.html`; Gradle 9.0 preferred mode and Gradle 10 default statement; `providers.exec`, `providers.fileContents`, `OperationCompletionListener` and `BuildEventsListenerRegistry`, `ExecOperations`, `notCompatibleWithConfigurationCache("reason")`; encryption key behaviour and `GRADLE_ENCRYPTION_KEY`; `cache-encryption-key` input; CI support status.
Fixed: the report path (it contains the hash twice); the advice to "start with warn, move to fail" (the default already fails; warn is for troubleshooting); the "Gradle 8.x: stable feature" sentence (replaced by the 9.0 and 10 statements).
Removed: the `org.gradle.configuration-cache.problems=warn` line from the default properties block and the claim that the cache is only per project directory beyond what the documentation states.
Method: documentation only; no commands were run.
