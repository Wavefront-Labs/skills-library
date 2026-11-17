---
id: computing-software.qa-testing-engineering.jest-pytest.junit-maven-surefire-failsafe-gradle
name: junit-maven-surefire-failsafe-gradle
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [maven-surefire, failsafe, gradle-test, junit-platform, junit5]
level: practitioner
status: docs-checked
description: "Run JUnit 5 with Maven Surefire (unit) and Failsafe (integration), and Gradle useJUnitPlatform: includes, tags, parallel forks, reports and failing the build correctly."
sources:
  - https://github.com/apache/maven-surefire/blob/master/maven-surefire-plugin/src/site/markdown/examples/junit-platform.md.vm
  - https://github.com/apache/maven-surefire/blob/master/maven-surefire-plugin/src/site/markdown/examples/inclusion-exclusion.md.vm
  - https://github.com/apache/maven-surefire/blob/master/maven-failsafe-plugin/src/main/java/org/apache/maven/plugin/failsafe/IntegrationTestMojo.java
  - https://github.com/gradle/gradle/blob/master/platforms/documentation/docs/src/docs/userguide/reference/platforms/jvm/java_testing.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running JUnit with Maven Surefire/Failsafe and Gradle

## Maven
```xml
<plugin>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>3.6.0</version>
  <configuration>
    <excludedGroups>integration,slow</excludedGroups>    <!-- JUnit 5 @Tag -->
    <forkCount>1C</forkCount>                              <!-- one JVM per core -->
    <reuseForks>true</reuseForks>
    <rerunFailingTestsCount>0</rerunFailingTestsCount>
  </configuration>
</plugin>
<plugin>
  <artifactId>maven-failsafe-plugin</artifactId>
  <version>3.6.0</version>
  <executions><execution><goals><goal>integration-test</goal><goal>verify</goal></goals></execution></executions>
</plugin>
```
- Surefire runs in `test` phase on `**/*Test.java`, `**/Test*.java`, `**/*Tests.java`, `**/*TestCase.java`.
- Failsafe runs in `integration-test` on `**/*IT.java`, `**/IT*.java`, `**/*ITCase.java`; `verify` fails the build **after** `post-integration-test` (so containers/servers get stopped).
- Skipping: `-DskipITs` skips Failsafe; since Surefire 3.6.0-M2 `-DskipTests` no longer skips Failsafe, and `-Dmaven.test.skip` skips both.
- Run: `mvn verify`; single test: `mvn test -Dtest=CartTest#addsItem`; tags: `-Dgroups=smoke`.
- Reports: `target/surefire-reports/*.xml` (JUnit XML) and `target/failsafe-reports/`.

## Gradle
```kotlin
tasks.test {
  useJUnitPlatform { excludeTags("integration") }
  maxParallelForks = (Runtime.getRuntime().availableProcessors() / 2).coerceAtLeast(1)
  testLogging { events("failed"); exceptionFormat = TestExceptionFormat.FULL }
}
val integrationTest by tasks.registering(Test::class) {
  useJUnitPlatform { includeTags("integration") }
  shouldRunAfter(tasks.test)
}
```
Single test: `./gradlew test --tests "com.acme.CartTest.addsItem"`. Reports: JUnit XML files under `build/test-results/<task>/` (one per test class) plus an HTML report.

## Gotchas
- Old Surefire (<2.22) does not see JUnit 5 tests: zero tests run and the build passes. Check "Tests run: N".
- Running integration tests with `mvn integration-test` (not `verify`) skips the failure check.
- `junit-jupiter-engine` must be on the test runtime classpath (the `junit-jupiter` aggregate includes it).
- Gradle skips an up-to-date test task; `./gradlew test --rerun` or `cleanTest test` forces a run.

## Verify
`mvn verify` reports unit and IT counts separately, and a failing IT fails the build after cleanup ran.

## Checked

Date: 2026-10-25. Documentation release: Maven Surefire/Failsafe 3.6.0 (GitHub master, last commit 2026-10-22) and Gradle 9.8.2 user guide sources.

Confirmed: default include patterns for Surefire (Test*, *Test, *Tests, *TestCase) and Failsafe (IT*, *IT, *ITCase); `groups`, `excludedGroups`, `forkCount` (the C suffix multiplies by CPU cores) and `reuseForks` parameters; Failsafe `integration-test` and `verify` goals; `skipITs` and the 3.6.0-M2 change to `-DskipTests`; JUnit 5 groups support since Surefire 2.22.0; report directories; Gradle `maxParallelForks` (default 1), `--tests`, `--rerun`, `cleanTest`, XML result location, tag filtering.

Removed as unconfirmed: the `build/reports/tests` HTML path and the pinned 3.5.2 version (now 3.6.0, the latest release tag at review).

Method: documentation only; no commands were run.
