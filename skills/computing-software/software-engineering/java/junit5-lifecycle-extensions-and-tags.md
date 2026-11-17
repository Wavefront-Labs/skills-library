---
id: computing-software.software-engineering.java.junit5-lifecycle-extensions-and-tags
name: junit5-lifecycle-extensions-and-tags
category: computing-software
field: software-engineering
product: java
tags: [java, junit5-extensions, junit-tags, test-lifecycle, tempdir, extendwith, java-testing]
level: practitioner
status: docs-checked
description: "Use JUnit 5 lifecycle, built-in extensions and tags: BeforeAll/BeforeEach, PER_CLASS instances, @TempDir, @Timeout, writing an Extension, and filtering suites by tag."
sources: ["https://junit.org/junit5/docs/current/user-guide/#writing-tests-test-instance-lifecycle", "https://junit.org/junit5/docs/current/user-guide/#extensions", "https://junit.org/junit5/docs/current/user-guide/#running-tests-tags"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JUnit 5 lifecycle, extensions and tags

**Goal:** shared setup without hidden coupling, reusable cross-cutting test behaviour,
and suites you can slice by speed or type.

## Lifecycle
```java
class RepoTest {
    @BeforeAll static void startDb() { ... }        // once per class (static unless PER_CLASS)
    @BeforeEach void reset() { ... }                // before every test
    @AfterEach void cleanup() { ... }
    @AfterAll static void stopDb() { ... }
}
```
A new instance is created **per test method** by default, so instance fields don't leak
between tests. `@TestInstance(Lifecycle.PER_CLASS)` shares one instance (non-static
`@BeforeAll`, useful with Kotlin) - then reset state explicitly.

## Built-in helpers
```java
@Test void writesFile(@TempDir Path dir) { ... }                 // deleted afterwards
@Test @Timeout(value = 2, unit = SECONDS) void fast() { ... }
@RepeatedTest(50) void noRace() { ... }
@Disabled("JIRA-123") @Test void flaky() { ... }
@EnabledOnOs(OS.LINUX) @EnabledIfEnvironmentVariable(named = "CI", matches = "true")
@DisplayName("rejects expired tokens")
```
Order is undefined unless `@TestMethodOrder(OrderAnnotation.class)`; tests depending on order
are a smell.

## Extensions
```java
public class FixedClockExtension implements BeforeEachCallback, ParameterResolver {
    private static final Clock CLOCK = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
    @Override public void beforeEach(ExtensionContext ctx) { /* e.g. set MDC, reset state */ }
    @Override public boolean supportsParameter(ParameterContext p, ExtensionContext c) {
        return p.getParameter().getType() == Clock.class; }
    @Override public Object resolveParameter(ParameterContext p, ExtensionContext c) { return CLOCK; }
}
@ExtendWith(FixedClockExtension.class)
class BillingTest { @Test void bills(Clock clock) { ... } }
```
Extension points: `Before/AfterAll|Each`, `BeforeTestExecution`, `ParameterResolver`,
`TestExecutionExceptionHandler`, `ExecutionCondition`, `TestWatcher`. Store per-test state in
`ctx.getStore(Namespace.create(getClass(), ctx.getRequiredTestMethod()))`, not static fields.
Compose: a custom annotation meta-annotated with `@ExtendWith` + `@Tag`.

## Tags and filtering
```java
@Tag("integration") class OrderRepositoryIT { ... }
```
```xml
<!-- surefire -->
<configuration><excludedGroups>integration | slow</excludedGroups></configuration>
```
```kotlin
tasks.test { useJUnitPlatform { excludeTags("integration") } }
```
Tag expressions support `!`, `&`, `|` and parentheses (plus `any()` and `none()`); a tag must not contain whitespace or ISO control characters.

## Parallel execution
```properties
# src/test/resources/junit-platform.properties
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
```
Guard shared resources with `@ResourceLock("db")` or `@Isolated`.

## Verify
- [ ] Unit suite excludes integration tags and runs in seconds; CI runs both.
- [ ] No test relies on execution order or static mutable state.

## Checked

Date: 2026-10-25. Documentation release: JUnit 6.1.3 (GitHub main, release of 2026-08-07).

Confirmed: per-method instances by default and PER_CLASS; `@TempDir`, `@Timeout`, `@RepeatedTest`, conditional annotations; extension interfaces; tag expression grammar and tag rules; parallel execution properties, `@ResourceLock`, `@Isolated`.

Removed as unconfirmed: the claim that IDE run configurations accept tag expressions.

Method: documentation only; no commands were run.
