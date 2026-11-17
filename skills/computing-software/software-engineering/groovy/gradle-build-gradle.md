---
id: computing-software.software-engineering.groovy.gradle-build-gradle
name: gradle-build-gradle
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, gradle-build-gradle, groovy-gradle-dsl]
level: practitioner
status: draft
description: "Gradle Groovy DSL basics: plugins block, repositories, dependencies, tasks, extra properties and the settings.gradle file."
sources:
  - https://docs.gradle.org/current/userguide/writing_build_scripts.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# build.gradle structure
```groovy
plugins { id 'java' }
repositories { mavenCentral() }
dependencies {
  implementation 'org.apache.commons:commons-lang3:3.14.0'   // illustrative version
  testImplementation 'junit:junit:4.13.2'
}
tasks.register('hello') { doLast { println 'hi' } }
```
- Files: `build.gradle` (project), `settings.gradle` (`rootProject.name = 'x'`, `include 'sub'`), `gradle.properties`.
- Groovy DSL allows `implementation 'g:a:v'` (no parentheses) and string/GString coordinates.
- Run with the wrapper: `./gradlew build`, `./gradlew tasks`, `--info`/`--stacktrace`.
- Kotlin DSL is the alternative; both can coexist across modules.

## Gotchas
- `apply plugin:` is legacy; prefer the `plugins {}` block.
- GString vs String coordinates matter for caching edge cases; use plain strings when no interpolation.

## Self-check
`./gradlew hello` prints `hi`.
