---
id: computing-software.qa-testing-engineering.test-automation.sonarqube-quality-gates
name: sonarqube-quality-gates
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [maintainability-metrics, sonarqube, code-smells, static-analysis, technical-debt, quality-gate, sonarcloud]
level: practitioner
status: draft
description: "Use SonarQube/SonarCloud for maintainability metrics: quality gates on new code, code smells, duplication, coverage import and tuning rules to cut noise."
sources:
  - https://docs.sonarsource.com/sonarqube-server/latest/user-guide/quality-gates/
  - https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/test-coverage/overview/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SonarQube quality gates and maintainability metrics

**Goal:** stop maintainability decay on new code without drowning in legacy findings. CTAL-TTA v4.0 3.2.3.

## Metrics
- **Maintainability rating** (A-E) from technical debt ratio (remediation effort / development cost).
- **Code smells**, **duplications** (% duplicated lines), **cognitive complexity**, **coverage**, **reliability** (bugs) and **security** (vulnerabilities, hotspots).

## Setup
```properties
# sonar-project.properties
sonar.projectKey=shop
sonar.sources=src
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.exclusions=**/generated/**
```
CI: run tests with coverage first, then `sonar-scanner` (or the Maven/Gradle plugin), then fail the job on gate status (`sonar.qualitygate.wait=true`).

## Quality gate ("Sonar way" style, on new code)
Coverage on new code >= 80%, duplicated lines on new code <= 3%, maintainability/reliability/security rating A, security hotspots reviewed 100%.

## Tuning
- Define "new code" (previous version or reference branch) so legacy debt does not block every PR.
- Disable rules that conflict with team conventions in a custom quality profile, not with blanket exclusions.
- Exclude generated code and test fixtures from duplication.

## Gotchas
- Coverage 0% in Sonar usually means report path wrong or report generated after the scan.
- Gate on overall code: legacy projects never pass, team stops looking.

## Verify
A PR introducing duplication or untested code shows the gate failing in the PR decoration.
