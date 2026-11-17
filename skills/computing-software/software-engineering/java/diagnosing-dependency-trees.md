---
id: computing-software.software-engineering.java.diagnosing-dependency-trees
name: diagnosing-dependency-trees
category: computing-software
field: software-engineering
product: java
tags: [java, dependency-tree, dependencyinsight, maven-enforcer, dependency-convergence, classpath-conflicts, java-dependency-hygiene]
level: practitioner
status: docs-checked
description: "Find why a library version is selected: mvn dependency:tree with includes and verbose, Gradle dependencies and dependencyInsight, and Maven Enforcer dependencyConvergence."
sources:
  - https://maven.apache.org/plugins/maven-dependency-plugin/tree-mojo.html
  - https://docs.gradle.org/current/userguide/viewing_debugging_dependencies.html
  - https://maven.apache.org/enforcer/enforcer-rules/dependencyConvergence.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Diagnosing dependency trees

**Goal:** answer "where does this version come from and why was it selected".

## Maven
```bash
mvn dependency:tree -Dincludes=<groupId>:<artifactId>
mvn dependency:tree -Dverbose
```
- `includes` (user property `includes`) filters the printed tree with a comma-separated list of patterns; each segment is optional and supports `*` wildcards, so `org.apache.*` matches every group id starting with `org.apache.`.
- `verbose` (default false) includes omitted nodes in the tree.

## Gradle
```bash
./gradlew dependencies --configuration <name>
./gradlew dependencyInsight --dependency <name> --configuration <name>
./gradlew buildEnvironment
./gradlew dependencies --scan
```
- `dependencies` renders the tree for all configurations of a project by default; it shows the selected version of each dependency and information on conflict resolution. `--configuration` focuses on one.
- `dependencyInsight` explains why a version was selected; `--dependency` and `--configuration` are both mandatory. Its report can say, for example, "By conflict resolution: between versions 1.7 and 1.6".
- `buildEnvironment` renders the buildscript classpath configuration.
- `--scan` adds a web-based, searchable dependency report.

## Prevent recurrence (Maven Enforcer)
Add the `dependencyConvergence` rule to the enforcer plugin. By default every convergence error is reported and any single error fails the build; optional parameters are `includes`, `excludes` (exceptions to includes) and `excludedScopes` (default excludes `provided` and `test`).

## Verify
- [ ] The tree shows the version you expect for the artifact in question.
- [ ] Enforcer `dependencyConvergence` passes in CI.

## Checked
2026-11-01. Confirmed against the maven-dependency-plugin tree goal page, the Gradle "Viewing and debugging dependencies" page and the Enforcer dependencyConvergence page. Removed as unconfirmed by those pages: the nearest-wins versus highest-wins claims, dependency:analyze and help:effective-pom, runtime class-source tricks, remediation advice (BOMs, exclusions, constraints), other enforcer rules, failOnVersionConflict and dependency locking.
Method: documentation only; no commands were run.
