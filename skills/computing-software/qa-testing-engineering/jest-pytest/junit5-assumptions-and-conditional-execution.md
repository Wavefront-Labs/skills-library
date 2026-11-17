---
id: computing-software.qa-testing-engineering.jest-pytest.junit5-assumptions-and-conditional-execution
name: junit5-assumptions-and-conditional-execution
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [assumptions, conditional-test-execution, enabledonos, disabledif, junit5]
level: practitioner
status: docs-checked
description: "Skip or enable JUnit 5 tests conditionally with Assumptions and annotations (EnabledOnOs, EnabledIfEnvironmentVariable, EnabledIfSystemProperty, Disabled, custom conditions)."
sources:
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/assumptions.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/conditional-test-execution.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/extensions/conditional-test-execution.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assumptions and conditional execution

## Assumptions (runtime)
```java
import static org.junit.jupiter.api.Assumptions.*;

@Test void runsOnlyOnCi() {
  assumeTrue("CI".equals(System.getenv("ENV")), "only on CI");
  // aborted (skipped) otherwise, not failed
}

@Test void partlyConditional() {
  assumingThat(isDockerAvailable(), () -> assertEquals(3, containerCount()));
  assertEquals(1, alwaysChecked());
}
```
A failed assumption throws `org.opentest4j.TestAbortedException`, so the test is aborted (reported as skipped), not failed.

## Annotations (declarative)
```java
@Test @EnabledOnOs({ OS.LINUX, OS.MAC }) void unixPaths() {}
@Test @DisabledOnOs(OS.WINDOWS) void symlinks() {}
@Test @EnabledOnJre(JRE.JAVA_21) void virtualThreads() {}
@Test @EnabledForJreRange(min = JRE.JAVA_17) void records() {}
@Test @EnabledIfEnvironmentVariable(named = "RUN_SLOW", matches = "true") void slowTest() {}
@Test @EnabledIfSystemProperty(named = "os.arch", matches = ".*64.*") void arch() {}
@Test @EnabledIf("dockerAvailable") void needsDocker() {}
boolean dockerAvailable() { return /* your own probe */ false; }   // condition method: boolean, no arguments
@Test @Disabled("JIRA-123: flaky on Windows") void temporarilyOff() {}
```

## Custom condition
```java
public class EnabledIfServiceUp implements ExecutionCondition {
  public ConditionEvaluationResult evaluateExecutionCondition(ExtensionContext ctx) {
    return ping() ? enabled("service up") : disabled("service down");
  }
}
@ExtendWith(EnabledIfServiceUp.class) class IntegrationTests {}
```

## Deactivating conditions
`junit.jupiter.conditions.deactivate=org.junit.*DisabledCondition` runs `@Disabled` tests (useful to check if they still fail).

## Gotchas
- Skipped tests are easy to forget: always give a reason (ticket id) and review the skipped count in CI.
- Assumptions based on environment can hide whole suites silently when CI env vars change; alert if skipped count spikes.

## Verify
CI report shows aborted tests with reasons; toggling the env var flips them to run.

## Checked

Date: 2026-10-25. Documentation release: JUnit 6.1.3 (GitHub main, release of 2026-08-07).

Confirmed: `Assumptions.assumeTrue(boolean, String)` and `assumingThat(boolean, Executable)` signatures in source; `TestAbortedException` package; the `@EnabledOnOs`, `@EnabledOnJre`, `@EnabledForJreRange`, `@EnabledIf` condition-method annotations; `junit.jupiter.conditions.deactivate` with the pattern `org.junit.*DisabledCondition`.

Removed as unconfirmed: the Testcontainers `DockerClientFactory` call (third-party API, not covered by the JUnit docs).

Method: documentation only; no commands were run.
