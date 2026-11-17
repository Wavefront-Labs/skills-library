---
id: computing-software.qa-testing-engineering.test-automation.test-observability-and-result-reporting
name: test-observability-and-result-reporting
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-observability, test-reporting, allure-report, test-analytics, flaky-tests, junit-xml]
level: practitioner
status: draft
description: "Report automation results for fast triage: JUnit XML, Allure or ReportPortal, history and trends, failure categorisation, flaky detection and traces linked to failures."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
  - https://allurereport.org/docs/
  - https://reportportal.io/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automation result reporting and test observability

**Goal:** when tests fail, people can tell within minutes whether it is a product defect, a test defect, environment or flakiness, and see trends over time.

## Layers of reporting
1. **Machine-readable results:** JUnit XML from every runner (`pytest --junitxml`, Playwright `junit` reporter, Maven Surefire), consumed by CI test summaries.
2. **Rich run reports:** Playwright HTML with traces, Allure (steps, attachments, history, categories), Cypress Cloud.
3. **Historical analytics:** ReportPortal, Allure TestOps, Datadog CI Visibility, BuildPulse/Trunk, or a home-built store of results (test name, duration, outcome, retry, commit, branch).

## Must-have features
- **Attachments on failure:** screenshot, video, trace, logs, request/response, with links from the CI summary.
- **History per test:** pass/fail sparkline, duration trend; recognise new failures vs long-standing.
- **Flaky detection:** passed-on-retry flagged and counted, not reported as green silently.
- **Failure categorisation:** Allure `categories.json` regex rules (e.g. timeout, element not found, 5xx) or ReportPortal auto-analysis; triage labels: product bug, automation bug, environment, flaky.
- **Ownership:** each test or folder mapped to a team (CODEOWNERS) so failures route automatically.
- **Correlation:** test run ID and trace ID in app logs (header `x-test-run-id`) so backend logs can be filtered to a failing test.

## Allure quick start (pytest)
`pip install allure-pytest && pytest --alluredir=allure-results` then `allure generate allure-results -o allure-report --clean`; keep `allure-report/history` between CI runs to get trends.

## Verify
For a random failure, a developer reaches the trace/screenshot and relevant logs from the CI page in under two minutes, and weekly trend data shows flake rate and slowest tests.
