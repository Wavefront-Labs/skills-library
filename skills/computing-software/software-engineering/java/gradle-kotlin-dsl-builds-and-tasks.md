---
id: computing-software.software-engineering.java.gradle-kotlin-dsl-builds-and-tasks
name: gradle-kotlin-dsl-builds-and-tasks
category: computing-software
field: software-engineering
product: java
tags: [java, java-build, gradle, gradle-kotlin-dsl, gradle-tasks, build-cache, configuration-cache, gradle-wrapper]
level: practitioner
status: docs-checked
description: "Write Gradle builds in the Kotlin DSL: plugins and java toolchains, dependency configurations, lazy task registration, build and configuration cache, wrapper hygiene."
sources:
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/dsl-apis/kotlin_dsl.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/platforms/jvm/toolchains.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/task-development/task_configuration_avoidance.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/optimizing-builds/configuration-cache/configuration_cache.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/runtime-configuration/build_environment.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/runtime-configuration/gradle_wrapper.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/core-plugins/java_library_plugin.adoc
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/core-plugins/application_plugin.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradle Kotlin DSL builds and tasks

**Goal:** a type-safe, fast Gradle build that IDEs understand and that caches well.

## 1. build.gradle.kts essentials
```kotlin
plugins {
    java
    application
}
java {
    toolchain { languageVersion = JavaLanguageVersion.of(21) }   // selects a matching local JDK; downloads one only if a toolchain download repository is configured
}
repositories { mavenCentral() }
dependencies {
    implementation(platform("org.springframework.boot:spring-boot-dependencies:<version>"))
    implementation("com.fasterxml.jackson.core:jackson-databind")
    api("com.google.guava:guava:<version>")          // needs the `java-library` plugin; exposed on consumers' compile classpath
    runtimeOnly("org.postgresql:postgresql:<version>")
    testImplementation(platform("org.junit:junit-bom:<version>"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")   // Gradle needs the JUnit Platform launcher declared
}
tasks.test { useJUnitPlatform() }
application { mainClass = "com.acme.MainKt" }
```
Configurations: `implementation` (compile+runtime, not exposed), `api` (exposed to consumers), `compileOnly`, `runtimeOnly`, `testImplementation`, `annotationProcessor`.

## 2. Tasks, lazily
```kotlin
val generateVersion by tasks.registering {
    val out = layout.buildDirectory.file("generated/version.txt")
    val ver = providers.gradleProperty("version").orElse("dev")
    inputs.property("version", ver)
    outputs.file(out)
    doLast { out.get().asFile.writeText(ver.get()) }
}
tasks.named<Jar>("jar") { from(generateVersion) }
```
- `tasks.register` / `named` (lazy) instead of `tasks.create` / `getByName` (eager).
- Declare inputs and outputs so up-to-date checks and the build cache work; use `Provider`s, never read files at configuration time.
- Wire tasks by passing task outputs as inputs (`from(generateVersion)`), not `dependsOn` alone.

## 3. Performance flags (gradle.properties)
```properties
org.gradle.caching=true
org.gradle.configuration-cache=true
org.gradle.parallel=true
org.gradle.jvmargs=-Xmx2g
```
`./gradlew build --scan` shows where time goes; `--dry-run`, `-m` show the task graph.

## 4. Commands
```bash
./gradlew build                     # assemble + check
./gradlew :api:test --tests '*OrderTest*'
./gradlew dependencies --configuration runtimeClasspath
./gradlew dependencyInsight --dependency jackson-databind
./gradlew wrapper --gradle-version 9.8.2 --distribution-type bin
```

## Gotchas
- Configuration cache fails on tasks that access `project` at execution time; fix with providers/injected services, or mark incompatible.
- `allprojects {}`/`subprojects {}` blocks couple projects and break isolation; use convention plugins.
- Commit `gradle/wrapper/gradle-wrapper.jar` and verify its checksum (`distributionSha256Sum`).
- Type-safe Kotlin DSL accessors are not available for plugins applied with `apply(plugin = ...)` in the script body, script plugins, or cross-project configuration; use the `plugins {}` block.

## Verify
- Second `./gradlew build` run reports tasks `UP-TO-DATE`/`FROM-CACHE`, and, with `org.gradle.configuration-cache=true`, later runs skip the configuration phase (see the configuration cache chapter).

## Checked

Date: 2026-10-25. Documentation release: Gradle 9.8.2 user guide sources (GitHub master; release of 2026-10-19).

Confirmed: toolchain auto-provisioning needs a configured download repository; `api` configuration from `java-library` is exported to consumers; `tasks.register` returns a lazy `TaskProvider`; properties `org.gradle.caching`, `org.gradle.parallel`, `org.gradle.configuration-cache` (default false), `org.gradle.jvmargs`; `--dry-run` / `-m`, `--scan`, `dependencyInsight --dependency ... --configuration ...`; wrapper `--gradle-version`, `--distribution-type` and `distributionSha256Sum`; JUnit Platform launcher must be declared for Jupiter tests; when type-safe accessors are unavailable; configuration cache rejects referencing `Project` at execution time.

Removed as unconfirmed: the Spotless plugin and its version, pinned dependency versions (now `<version>` placeholders), `-XX:+UseParallelGC`, and the exact "Configuration cache entry reused" message.

Method: documentation only; no commands were run.
