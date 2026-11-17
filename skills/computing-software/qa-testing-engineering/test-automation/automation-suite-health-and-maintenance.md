---
id: computing-software.qa-testing-engineering.test-automation.automation-suite-health-and-maintenance
name: automation-suite-health-and-maintenance
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [suite-health, automation-maintenance, test-automation-strategy, test-suite-metrics, flaky-rate, test-runtime-budget, flake-rate]
level: practitioner
status: draft
description: "Keep an automation suite healthy: track runtime, flake rate, failure triage time and maintenance cost, and schedule refactoring and pruning."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
  - https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automation suite health and maintenance

**Goal:** a suite that the team trusts and can afford to maintain.

## Health metrics (weekly)
| Metric | Target (example) | Source |
|---|---|---|
| Pipeline suite runtime | < 15 min PR, < 60 min full | CI timings |
| Flake rate (tests passing on retry / total) | < 1% of runs | retry data, Cypress/Playwright reports |
| Red build time to triage | < 1 working day | CI + ticket |
| Real-defect ratio of failures | high; failures mostly real bugs | triage labels |
| Maintenance hours / sprint | trend stable | time tracking or tickets |
| Tests disabled/skipped | trending down | `grep -r "skip"`, reports |

## Practices
- Every failure triaged: product bug, test bug, environment, flaky. Label it; patterns drive fixes.
- Budget maintenance time each sprint (e.g. 10-20% of automation effort).
- Refactor duplicated helpers into the adaptation layer; delete dead page objects.
- Review skipped/quarantined tests monthly: fix or delete.
- Upgrade tools regularly in small steps (Playwright, browsers, drivers) instead of huge yearly jumps.

## Gotchas
- A suite red most of the time trains people to ignore it ("it's always red"); restore green quickly, even by quarantining.
- Counting tests as a success metric encourages low-value tests.

## Verify
A dashboard (Allure, ReportPortal, CI analytics or a spreadsheet) with these metrics trending in the right direction.
