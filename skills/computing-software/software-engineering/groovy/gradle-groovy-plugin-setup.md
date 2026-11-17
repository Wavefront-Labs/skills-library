---
id: computing-software.software-engineering.groovy.gradle-groovy-plugin-setup
name: gradle-groovy-plugin-setup
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, gradle-groovy-plugin-setup, groovy-gradle-plugin]
level: practitioner
status: docs-checked
description: "Build Groovy projects with Gradle: the groovy plugin, source sets, groovydoc, and classpath configuration."
sources:
  - https://docs.gradle.org/current/userguide/groovy_plugin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# groovy plugin tasks and source sets
```groovy
plugins { id 'groovy' }
repositories { mavenCentral() }
dependencies {
  implementation 'org.apache.groovy:groovy:<version>'   // declare Groovy explicitly; pick the current version
}
```
- The plugin extends the Java plugin and supports joint compilation: Groovy and Java can reference each other in both directions.
- Source dirs: `src/main/groovy` and `src/test/groovy` (plus `src/<sourceSet>/groovy`) may contain Groovy and Java code; `src/main/java` and `src/test/java` may only contain Java. None of them need to exist.
- Tasks: `compileGroovy` (depends on `compileJava`), `compileTestGroovy` (depends on `compileTestJava`), `groovydoc`; `classes` depends on `compileGroovy`.
- Change the layout with `sourceSets { main { groovy { srcDirs = ['src/groovy'] } } }`.
- Groovy projects must declare a Groovy dependency (`implementation` for production code, `testImplementation` for test-only). `localGroovy()` uses the Groovy that ships with Gradle, which differs between Gradle versions, so it is less safe.
- `GroovyCompile` and `Groovydoc` infer `groovyClasspath` from the task classpath (a `groovy-all` or `groovy` jar); if none is found the task fails saying it could not be inferred.

## Gotchas
- Because `compileGroovy` depends on `compileJava`, Java files in `src/main/java` are compiled first and cannot use Groovy classes; to mix both ways put the Java files under `src/main/groovy`.
- Gradle's own Groovy is separate from your project's; declare the dependency explicitly.

## Self-check
`./gradlew compileGroovy` succeeds for a project with a Groovy class under `src/main/groovy`.

## Checked
2026-11-09. Confirmed against the Gradle Groovy plugin page (tasks and dependencies, layout, joint compilation, Groovy dependency, localGroovy, groovyClasspath inference). Removed: Spock artifact coordinates and `useJUnitPlatform()`, the example Groovy version, and the `build/classes/groovy/main` output path, which the page does not state.
Method: documentation only; no commands were run.
