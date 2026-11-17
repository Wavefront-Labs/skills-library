---
id: computing-software.software-engineering.java.surefire-failsafe-and-gradle-test-tasks
name: surefire-failsafe-and-gradle-test-tasks
category: computing-software
field: software-engineering
product: java
tags: [java, surefire, failsafe, integration-tests, gradle-test, jvm-test-suite, java-testing]
level: practitioner
status: docs-checked
description: "Run Java tests in builds: Surefire for unit tests, Failsafe for *IT integration tests with verify, forking and parallelism, and Gradle test tasks and JVM test suites."
sources: ["https://maven.apache.org/surefire/maven-surefire-plugin/", "https://maven.apache.org/surefire/maven-failsafe-plugin/", "https://docs.gradle.org/current/userguide/java_testing.html", "https://docs.gradle.org/current/userguide/jvm_test_suite_plugin.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Surefire, Failsafe and Gradle test tasks

**Goal:** unit and integration tests wired into the build lifecycle so integration
failures still let containers and servers shut down, and reports land in CI.

## Maven: two plugins, two phases
- **Surefire** (`test` phase): runs `**/*Test.java`, `**/Test*.java`, `**/*Tests.java`, `**/*TestCase.java`.
- **Failsafe** (`integration-test` + `verify` phases): runs `**/*IT.java`, `**/IT*.java`,
  `**/*ITCase.java`. Failures are recorded in `integration-test` and only fail the build in
  `verify`, so `post-integration-test` cleanup (stopping servers) still runs.
```xml
<plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-failsafe-plugin</artifactId>
  <executions><execution><goals><goal>integration-test</goal><goal>verify</goal></goals></execution></executions>
</plugin>
```
Run `mvn verify`, not `mvn integration-test` (which skips the verify check).

## Common commands
```bash
mvn test -Dtest=OrderServiceTest#rejectsEmpty      # single method
mvn verify -Dit.test=OrderRepositoryIT
mvn verify -DskipITs                                # unit only (since 3.6.0-M2, -DskipTests no longer skips Failsafe)
mvn test -Dsurefire.failIfNoSpecifiedTests=false    # multi-module single-test runs
mvn test -Dsurefire.rerunFailingTestsCount=2        # a failure that passes on rerun is reported as a flake
```
Reports: `target/surefire-reports/*.xml` and `target/failsafe-reports/` (JUnit XML for CI).

## Forking and parallelism
```xml
<configuration>
  <forkCount>1C</forkCount>                 <!-- one JVM per core -->
  <reuseForks>true</reuseForks>
  <argLine>@{argLine} -Xmx1g</argLine>
</configuration>
```
`@{argLine}` is late property replacement: it picks up an `argLine` property that another plugin modified during the build (and becomes empty if the property is undefined). For hung forks set `forkedProcessExitTimeoutInSeconds`.

## Gradle
```kotlin
tasks.test {
    useJUnitPlatform()
    maxParallelForks = (Runtime.getRuntime().availableProcessors() / 2).coerceAtLeast(1)
    testLogging { events("failed"); exceptionFormat = TestExceptionFormat.FULL }
}
testing {
    suites {
        register<JvmTestSuite>("integrationTest") {
            dependencies { implementation(project()) }
            targets { all { testTask.configure { shouldRunAfter(tasks.test) } } }
        }
    }
}
tasks.check { dependsOn(testing.suites.named("integrationTest")) }
```
`./gradlew test --tests '*OrderServiceTest.rejects*'`, `--rerun` to force the task to run again
(or `cleanTest test`). A test task whose inputs are unchanged is up to date and skipped.

## Verify
- [ ] CI runs `mvn verify` / `./gradlew check` and publishes JUnit XML reports.
- [ ] Integration tests live in `*IT` classes or a separate suite, not mixed into the unit run.

## Checked

Date: 2026-10-25. Documentation release: Maven Surefire/Failsafe 3.6.0 (GitHub master, last commit 2026-10-22) and Gradle 9.8.2 user guide sources.

Confirmed: Surefire and Failsafe default includes; Failsafe goals and `skipITs`; `it.test`, `-Dtest=Class#method`, `surefire.failIfNoSpecifiedTests` (default true) and `surefire.rerunFailingTestsCount` (default 0) properties; flake reporting; `forkCount` 1C, `reuseForks`, `@{...}` late replacement in argLine; `forkedProcessExitTimeoutInSeconds`; Gradle `maxParallelForks`, `testLogging`, `--tests`, `--rerun`, JVM Test Suite `register<JvmTestSuite>`, `targets.all`/`testTask`, `shouldRunAfter`, `tasks.check` dependency, `implementation(project())` for non-default suites.

Removed as unconfirmed: the JaCoCo-specific wording, `-XX:+EnableDynamicAgentLoading`, the jstack advice, the Testcontainers dependency line and the `--continue` remark.

Method: documentation only; no commands were run.
