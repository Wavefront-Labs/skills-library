---
id: computing-software.software-engineering.java.junit5-parallel-test-execution
name: junit5-parallel-test-execution
category: computing-software
field: software-engineering
product: java
tags: [java, junit5, junit-parallel-execution, resourcelock, test-isolation, execution-mode]
level: practitioner
status: docs-checked
description: "Run JUnit 5 tests in parallel safely: junit-platform.properties, same-thread vs concurrent mode, @ResourceLock and @Isolated."
sources: ["https://junit.org/junit5/docs/current/user-guide/#writing-tests-parallel-execution"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel test execution

## In-JVM
By default JUnit Jupiter runs tests sequentially in a single thread; parallel execution is opt-in. Enabling `junit.jupiter.execution.parallel.enabled` is only the first step: classes and methods still run sequentially until their execution mode is changed. `src/test/resources/junit-platform.properties`:
```properties
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.mode.default = same_thread
junit.jupiter.execution.parallel.mode.classes.default = concurrent
junit.jupiter.execution.parallel.config.strategy = dynamic
junit.jupiter.execution.parallel.config.dynamic.factor = 1
```
Modes: `SAME_THREAD` forces execution in the parent's thread; `CONCURRENT` runs concurrently unless a resource lock forces the same thread. The default mode is `SAME_THREAD`. The properties above run classes concurrently and methods sequentially, with parallelism computed by the dynamic strategy as a factor times the available processors. Override per element with `@Execution(ExecutionMode.CONCURRENT)`.

Test classes that use `Lifecycle.PER_CLASS` or a `MethodOrderer` are exceptions to the default mode: their methods run concurrently only if `@Execution(CONCURRENT)` is present on the class or method, and with PER_CLASS you must make the class thread-safe.

## Synchronizing shared resources
```java
@ResourceLock(value = Resources.SYSTEM_PROPERTIES, mode = ResourceAccessMode.READ_WRITE)
@Test void usesSystemProps() { ... }
@Isolated class SchemaMigrationTest {}        // runs sequentially with no other tests running
```
`@ResourceLock` names a shared resource (user-defined string or a constant from `Resources`: `SYSTEM_PROPERTIES`, `SYSTEM_OUT`, `SYSTEM_ERR`, `LOCALE`, `TIME_ZONE`). Two tests needing `READ` access may run in parallel; `READ_WRITE` excludes all others on that resource. The lock is acquired before `@BeforeEach` methods and released after `@AfterEach` methods. Without a lock, tests that write then read a shared system property are flaky when run in parallel.

## Verify
Run the suite several times in parallel mode and compare results; log `Thread.currentThread().getName()` in a sample test to confirm concurrency.

## Checked

Method: docs-checked 2026-11-09 against the JUnit 5 user guide Parallel Execution page (mode defaults, PER_CLASS and MethodOrderer exceptions, strategies, ResourceLock, Resources constants, Isolated). The Surefire and Gradle pages were not read; dropped their forkCount and maxParallelForks claims, plus unconfirmed advice on shared statics, ports, Spring context caching and DirtiesContext.
