---
id: computing-software.software-engineering.java.code-coverage-with-jacoco
name: code-coverage-with-jacoco
category: computing-software
field: software-engineering
product: java
tags: [java, jacoco, code-coverage, coverage-thresholds, branch-coverage, aggregate-report, java-testing, java-code-quality]
level: practitioner
status: docs-checked
description: "Measure Java coverage with JaCoCo in Maven and Gradle: agent setup, unit plus integration merges, multi-module aggregate reports, coverage gates and exclusions."
sources: ["https://www.jacoco.org/jacoco/trunk/doc/maven.html", "https://docs.gradle.org/current/userguide/jacoco_plugin.html", "https://www.jacoco.org/jacoco/trunk/doc/counters.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Code coverage with JaCoCo

**Goal:** trustworthy coverage numbers (including integration tests) and a gate that
prevents regressions without encouraging junk tests.

## Maven
```xml
<plugin>
  <groupId>org.jacoco</groupId><artifactId>jacoco-maven-plugin</artifactId><version>0.8.15</version>
  <executions>
    <execution><id>prepare</id><goals><goal>prepare-agent</goal></goals></execution>
    <execution><id>prepare-it</id><goals><goal>prepare-agent-integration</goal></goals></execution>
    <execution><id>report</id><phase>verify</phase><goals><goal>report</goal><goal>report-integration</goal></goals></execution>
    <execution><id>check</id><goals><goal>check</goal></goals>
      <configuration><rules><rule><element>BUNDLE</element><limits>
        <limit><counter>BRANCH</counter><value>COVEREDRATIO</value><minimum>0.70</minimum></limit>
      </limits></rule></rules></configuration></execution>
  </executions>
</plugin>
```
`prepare-agent` sets the `argLine` property (or `tycho.testArgLine` for eclipse-test-plugin packaging); if you also set `<argLine>` in Surefire, start it with `@{argLine}`, e.g.
`@{argLine} -Xmx1g`, or the agent is dropped and the goals report "Skipping JaCoCo execution
due to missing execution data file". `report` writes to `target/site/jacoco` and `prepare-agent-integration` to `jacoco-it.exec`.

Multi-module: a dedicated `coverage` module depending on all others with the `report-aggregate`
goal.

## Gradle
```kotlin
plugins { jacoco }
tasks.test { finalizedBy(tasks.jacocoTestReport) }
tasks.jacocoTestReport { dependsOn(tasks.test); reports { xml.required = true } }
tasks.jacocoTestCoverageVerification {
    violationRules { rule { limit { counter = "BRANCH"; minimum = "0.70".toBigDecimal() } } }
}
tasks.check { dependsOn(tasks.jacocoTestCoverageVerification) }
```
The `jacocoTestReport` task does not depend on `test` (hence `finalizedBy` above), and `jacocoTestCoverageVerification` is not wired into `check` automatically. The HTML report goes to `reports/jacoco/test/html` under the build directory. Aggregate across subprojects with the `jacoco-report-aggregation` plugin.

## Counters
INSTRUCTION, BRANCH, LINE, COMPLEXITY, METHOD, CLASS (see the counters page for definitions).

## Exclusions
```xml
<configuration><excludes><exclude>**/generated/**</exclude><exclude>**/*Application.class</exclude></excludes></configuration>
```
JaCoCo automatically filters classes and methods annotated with any annotation whose simple name contains
`Generated` and whose retention is CLASS or RUNTIME.

## Using the numbers
- Gate on "don't decrease" (diff coverage in PRs via Codecov/Sonar) rather than a high absolute
  number on legacy code.
- 100% coverage does not mean tested assertions; mutation testing (PIT) checks test strength.

## Verify
- [ ] `target/site/jacoco/index.html` (Maven) or the `reports/jacoco` build folder (Gradle) shows non-zero integration coverage when ITs exist.
- [ ] XML report uploaded to the coverage service in CI.

## Checked

Date: 2026-10-25. Documentation release: JaCoCo 0.8.15 (released 2026-06-04) and Gradle 9.8.2 user guide sources.

Confirmed: goals `prepare-agent` (phase initialize), `prepare-agent-integration` (pre-integration-test, `jacoco-it.exec`), `report`, `check` (verify) and rule elements BUNDLE / BRANCH / COVEREDRATIO; `@{argLine}` late replacement and the "Skipping JaCoCo execution due to missing execution data file" message; the `Generated` annotation filter; Gradle `jacocoTestReport` not depending on `test`, `JacocoCoverageVerification` not wired into `check`, default tool version 0.8.15, `jacoco-report-aggregation` plugin id.

Removed as unconfirmed: the Lombok configuration key and the claim that branch coverage is the most informative counter (opinion).

Method: documentation only; no commands were run.
