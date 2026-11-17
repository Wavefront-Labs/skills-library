---
id: computing-software.qa-testing-engineering.jest-pytest.junit5-tempdir-timeouts-repeated
name: junit5-tempdir-timeouts-repeated
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [tempdir, repeatedtest, junit-timeout, assert-timeout, junit5]
level: practitioner
status: docs-checked
description: "Use JUnit 5 @TempDir for isolated files, @Timeout and assertTimeoutPreemptively for hangs, and @RepeatedTest to probe flakiness, with their lifecycle and parallel caveats."
sources:
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/built-in-extensions.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/timeouts.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/repeated-tests.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeouts, TempDir and repeated tests

## @TempDir
```java
@Test void writesReport(@TempDir Path dir) throws IOException {
  Path out = dir.resolve("report.csv");
  Report.write(out);
  assertThat(Files.readAllLines(out)).first().isEqualTo("id,total");
}
@TempDir static Path shared;     // per class (static) - shared by all tests in the class
```
Deleted after the test/class by default (`CleanupMode.ALWAYS`). `@TempDir(cleanup = CleanupMode.ON_SUCCESS)` keeps it on failure for debugging; `NEVER` always keeps it. The default can be changed with `junit.jupiter.tempdir.cleanup.mode.default`.

## Timeouts
```java
@Test @Timeout(value = 500, unit = TimeUnit.MILLISECONDS) void fast() { ... }
@Test void bounded() {
  assertTimeout(Duration.ofSeconds(2), () -> service.call());              // waits for completion, then checks
  String r = assertTimeoutPreemptively(Duration.ofSeconds(2), () -> service.call()); // aborts at 2s
}
```
- `@Timeout` on a class applies to all test methods; default for all testable and lifecycle methods: `junit.jupiter.execution.timeout.default=30s` (format `<number> [ns|μs|ms|s|m|h|d]`, more specific `...test.method.default` parameters override it).
- `assertTimeoutPreemptively` runs the code in another thread: ThreadLocal-dependent code (Spring transactions, some mocks) breaks.
- `@Timeout` runs in the test thread by default (`SAME_THREAD`: the thread is interrupted on timeout); `@Timeout(threadMode = SEPARATE_THREAD)` has the same trade-off as `assertTimeoutPreemptively`.
- Disable during debugging: `junit.jupiter.execution.timeout.mode=disabled_on_debug`.

## @RepeatedTest
```java
@RepeatedTest(value = 50, name = "{displayName} {currentRepetition}/{totalRepetitions}", failureThreshold = 1)
void raceFree(RepetitionInfo info) { ... }
```
`failureThreshold` stops after N failures. Good for reproducing flakiness locally; don't leave 50x repeats in the suite.

## Gotchas
- A `static` `@TempDir` field is shared by all tests in the class; use an instance field or constructor/method injection for per-test isolation.
- Timeouts too tight fail on slow CI agents; set them as hang detectors (10x normal), not performance tests.

## Verify
A deliberately hanging test fails at the timeout with a timeout failure message; temp dirs are gone after the run.

## Checked

Date: 2026-10-25. Documentation release: JUnit 6.1.3 (GitHub main, release of 2026-08-07).

Confirmed: TempDir cleanup modes and default parameter; static versus instance field sharing; `@Timeout` thread modes and the ThreadLocal rationale; `junit.jupiter.execution.timeout.default` and its more specific variants; `timeout.mode` values `enabled`, `disabled`, `disabled_on_debug`; `@RepeatedTest(failureThreshold)` (since 5.10, default Integer.MAX_VALUE); `RepetitionInfo`.

Removed as unconfirmed: the `junit.jupiter.tempdir.scope=per_context` parameter, the PER_CLASS TempDir claim and the exact timeout message text, none of which appear in the user guide.

Method: documentation only; no commands were run.
