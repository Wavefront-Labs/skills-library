---
id: computing-software.devops-ci-cd.gradle.gradle-java-testing-configuration
name: gradle-java-testing-configuration
category: computing-software
field: devops-ci-cd
product: gradle
tags: [testing, junit-platform, test-filtering, max-parallel-forks, fork-every, integration-tests, fail-fast]
level: practitioner
status: docs-checked
description: "Configure Gradle Test tasks: JUnit Platform, filtering, parallel forks, reports, logging, integration test source sets and fail-fast."
sources: ["https://docs.gradle.org/current/userguide/java_testing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradle java testing configuration

Enable the JUnit Platform:

```kotlin
dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.7.1")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
tasks.named<Test>("test") { useJUnitPlatform() }
```

Filtering: `./gradlew test --tests SomeTestClass.someSpecificMethod` or `filter { includeTestsMatching("*IntegTest") }`. Patterns beginning with an uppercase letter match simple class or method names; `*` is a plain wildcard.

Forking: `maxParallelForks` (default 1) runs test classes in parallel JVMs, so tests must be isolated; `org.gradle.test.worker` gives each process a unique value for resource names. `forkEvery` (default 0) starts a fresh JVM after N classes, useful for leaky tests but slower when low.

Reports and logging: HTML report, JUnit XML and binary results by default. Locations come from `reporting.baseDirectory` and `java.testResultsDir`; `reports { junitXml.isOutputPerTestCase = true; junitXml.mergeReruns = true }` adjusts XML. `testLogging { events("passed", "failed", "skipped") }` controls console events.

Integration tests: create an `intTest` source set and a `Test` task with `testClassesDirs = sourceSets["intTest"].output.classesDirs`, `classpath = sourceSets["intTest"].runtimeClasspath`, `shouldRunAfter("test")`, then `tasks.check { dependsOn(integrationTest) }`. The incubating JVM Test Suite plugin (`testing.suites.named("test", JvmTestSuite::class) { useJUnitJupiter() }`) configures frameworks per suite.

`failFast = true` (or `--fail-fast`) stops at the first failure. Force a rerun with `./gradlew test --rerun` or `cleanTest test`.

## Checked

2026-11-04. Confirmed against the Gradle user guide page listed in `sources` (flags, property names, defaults, limits and the behaviour described). Removed: nothing.
Method: documentation only; no commands were run.
