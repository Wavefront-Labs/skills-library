---
id: computing-software.qa-testing-engineering.jest-pytest.junit5-dynamic-tests-tags-parallel
name: junit5-dynamic-tests-tags-parallel
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [dynamic-tests, junit-parallel, junit5, testfactory, junit-tags]
level: practitioner
status: docs-checked
description: "Use JUnit 5 dynamic tests with @TestFactory, tag and filter tests in Maven and Gradle, and enable parallel execution with resource locks and safe configuration."
sources:
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/dynamic-tests.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/running-tests/tags.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/parallel-execution.adoc
  - https://github.com/apache/maven-surefire/blob/master/maven-surefire-plugin/src/main/java/org/apache/maven/plugin/surefire/SurefireMojo.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic tests, tags and parallel execution (JUnit 5)

## Dynamic tests
```java
@TestFactory
Stream<DynamicTest> everyFixtureFileParses() throws IOException {
  return Files.list(Path.of("src/test/resources/invoices"))
      .map(p -> dynamicTest(p.getFileName().toString(), () -> assertDoesNotThrow(() -> InvoiceParser.parse(p))));
}

@TestFactory
Stream<DynamicContainer> rulesByCountry() {
  return Rules.countries().stream().map(c ->
      dynamicContainer(c, Rules.cases(c).stream().map(k -> dynamicTest(k.name(), () -> assertEquals(k.expected(), Vat.of(k))))));
}
```
Generated at runtime from data (files, DB, API). There are no lifecycle callbacks for individual dynamic tests: `@BeforeEach`/`@AfterEach` run around the factory method, not each dynamic test.

## Tags
```java
@Tag("integration") @Tag("slow")
class PaymentGatewayIT { ... }
```
Maven Surefire: `mvn test -Dgroups="fast & !flaky"` / `-DexcludedGroups=slow`.
Gradle:
```kotlin
tasks.test { useJUnitPlatform { includeTags("fast"); excludeTags("slow", "flaky") } }
tasks.register<Test>("integrationTest") { useJUnitPlatform { includeTags("integration") } }
```
Tag expressions support `!`, `&`, `|`, parentheses, and the special `any()` and `none()`.

## Parallel execution
```properties
# src/test/resources/junit-platform.properties
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.mode.classes.default=concurrent
junit.jupiter.execution.parallel.config.strategy=dynamic
junit.jupiter.execution.parallel.config.dynamic.factor=1
```
Control per class/method:
```java
@Execution(ExecutionMode.SAME_THREAD) class LegacyStaticStateTest { ... }
@ResourceLock(value = "system-properties", mode = READ_WRITE) @Test void setsLocale() { ... }
@Isolated class ChangesGlobalClockTest { ... }
```
Alternative: Surefire/Gradle fork-level parallelism (`forkCount`, `maxParallelForks`) isolates JVM state at higher cost.

## Gotchas
- Static/shared state (singletons, system properties, shared DB rows) breaks under concurrency; fix or lock.
- Dynamic tests are not parameterized tests: lifecycle callbacks differ; prefer `@ParameterizedTest` for fixed data sets.

## Verify
Tagged subsets run in separate CI stages, and the suite passes repeatedly with parallel mode enabled.

## Checked

Date: 2026-10-25. Documentation release: JUnit 6.1.3 (GitHub main, release of 2026-08-07) and Surefire 3.6.0.

Confirmed: no lifecycle callbacks per dynamic test; `dynamicContainer` and `dynamicTest` API; tag expression operators; `-Dgroups` / `-DexcludedGroups` Surefire properties; parallel parameters (`enabled`, `mode.default`, `mode.classes.default`, `config.strategy`, `config.dynamic.factor`) and `@Isolated`, `@ResourceLock` with `READ_WRITE`; Gradle `maxParallelForks` and Surefire `forkCount`.

Method: documentation only; no commands were run.
