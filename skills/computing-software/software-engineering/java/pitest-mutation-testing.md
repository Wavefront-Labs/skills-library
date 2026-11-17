---
id: computing-software.software-engineering.java.pitest-mutation-testing
name: pitest-mutation-testing
category: computing-software
field: software-engineering
product: java
tags: [java, java-code-quality, pitest-mutation-testing, pit, mutation-score, test-quality]
level: advanced
status: docs-checked
description: "Measure test strength with PIT mutation testing: Maven goal, targeting classes, thresholds, history for incremental runs, mutator groups."
sources: ["https://pitest.org/quickstart/maven/", "https://pitest.org/quickstart/mutators/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PIT mutation testing

Line coverage says code ran, not that tests would notice a bug. PIT changes the bytecode, reruns the covering tests, and reports mutants **killed** (a test failed) vs **survived** (tests still pass: a gap).

## Setup (Maven)
```xml
<plugin><groupId>org.pitest</groupId><artifactId>pitest-maven</artifactId>
  <configuration>
    <targetClasses><param>com.acme.billing.*</param></targetClasses>
    <mutationThreshold>80</mutationThreshold>
  </configuration></plugin>
```
```bash
mvn test-compile org.pitest:pitest-maven:mutationCoverage     # HTML report under target/pit-reports/ in a timestamped folder
mvn -DwithHistory test-compile org.pitest:pitest-maven:mutationCoverage   # reuse history to speed up repeated analysis
```
- `targetClasses` takes globs. Matching an exact class name excludes inner classes; end with `*` (`com.package.Class*`) or add a second rule. Since pitest 1.2.0, if `targetClasses` is omitted pitest scans the project for classes; before that it assumed a package matching the group id.
- `mutationThreshold` is the percentage of killed mutants at which to fail the build; the page warns that equivalent mutations make threshold choice a matter of careful thought. `coverageThreshold` and `testStrengthThreshold` (killed / (killed + survived)) also exist. Thresholds default to integer precision; set `thresholdPrecision` above 0 for decimals, otherwise small regressions can go unnoticed.
- `withHistory` points the history input and output files to a project-specific file in the temp directory for local speed-ups.
- `timeoutFactor` (default 1.25) and `timeoutConstant` decide when a mutated test is considered stuck in an infinite loop.
- Mutator groups include OLD_DEFAULTS, DEFAULTS, STRONGER and ALL; start with DEFAULTS or STRONGER rather than ALL.

## Reading results
For each survivor, open the report line and decide: add an assertion, add a boundary test, or accept it as an equivalent mutant. Exclude noise with `excludedClasses` or `avoidCallsTo` (for example logger classes).

## Gotchas
- Mutation analysis is slow: target the domain packages only.
- Mutation score is a tool for finding weak tests, not a target to game.

## Checked

Method: docs-checked 2026-11-09 against the pitest.org Maven quickstart (mutationCoverage goal, targetClasses and globs, withHistory, thresholds, timeoutFactor, avoidCallsTo, excludedClasses) and the mutators page (group table). The Gradle quickstart page did not yield usable content, so it is dropped as a source. Dropped unconfirmed claims (plugin versions, JUnit 5 plugin dependency, Gradle plugin id, scmMutationCoverage, @Generated, flaky-test advice).
