---
id: computing-software.software-engineering.groovy.gradle-groovy-closures
name: gradle-groovy-closures
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, gradle-groovy-closures]
level: advanced
status: draft
description: "How Gradle configuration blocks are closures with delegates, plus the ext properties, task configuration avoidance and Groovy gotchas."
sources:
  - https://docs.gradle.org/current/userguide/writing_build_scripts.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Closures and delegation in Gradle scripts
- A block like `dependencies { ... }` is a closure delegated to the `DependencyHandler`; `it` is not the delegate.
- Use `tasks.register` (lazy) over `task` (eager) for faster configuration.
- Extra properties: `ext.version = '1'` / `ext { x = 1 }`, read as `project.ext.x` or `x`; prefer `gradle.properties` or version catalogs (`gradle/libs.versions.toml`).
- Task types: `tasks.register('zipIt', Zip) { from 'src'; archiveFileName = 'a.zip' }`.
- Conditional logic is plain Groovy: `if (project.hasProperty('x')) { ... }`.

## Gotchas
- Closure `delegate` surprises: inside `doLast { }`, `project` and `task` resolve differently than at configuration time.
- `project.hasProperty` vs provider API (`providers.gradleProperty`) differs for configuration cache.

## Self-check
Run `./gradlew help --task hello` and confirm configuration is lazy (`--info` shows no creation until needed).
