---
id: computing-software.devops-ci-cd.gradle.gradle-performance-properties
name: gradle-performance-properties
category: computing-software
field: devops-ci-cd
product: gradle
tags: [performance, org-gradle-parallel, jvmargs, incremental-build, build-scan, repositories-order]
level: practitioner
status: docs-checked
description: "Tune Gradle build speed with the gradle.properties switches, incremental task declarations, Build Scan views and configuration hygiene."
sources: ["https://docs.gradle.org/current/userguide/performance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle performance properties

`gradle.properties` switches:
- `org.gradle.parallel=true` runs tasks from different subprojects concurrently (`org.gradle.tooling.parallel`, since 9.4.0, controls Tooling API parallelism separately).
- `org.gradle.caching=true` enables the build cache.
- `org.gradle.daemon=true` (default) keeps a background JVM.
- `org.gradle.configuration-cache=true` skips configuration when inputs are unchanged.
- `org.gradle.jvmargs=-Xmx2048M` raises the heap; the 512MB default suits most projects.

Incremental builds: declare task inputs and outputs (`inputs.files(...)`, `outputs.dir(...)`) so Gradle can skip up-to-date tasks; most built-in tasks already do.

Build Scan views: Timeline (parallelism bottlenecks and why tasks ran), Build Cache tab (hits and transfer rates), Task Execution (non-cacheable tasks), Dependency resolution (resolution during configuration), Network Activity (slow downloads) and Tests (ranked by duration).

Other tips from the guide:
- Update Gradle, Java and plugins.
- Avoid expensive work during configuration, such as network calls in `apply()` or task constructors.
- Apply plugins only where needed and move shared logic into `buildSrc`.
- Avoid dynamic (`1.+`) and snapshot versions; put the most-used repository first and keep the count low.
- Prefer `implementation` over `api` for internal dependencies.
- Tune tests with `maxParallelForks`, `forkEvery`, and disabled reports; fork Java compilation with `options.fork = true`.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
