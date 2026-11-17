---
id: computing-software.qa-testing-engineering.test-case-design.quality-dashboards
name: quality-dashboards
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [quality-dashboard, test-reporting, test-metrics, grafana, allure, ci-analytics]
level: practitioner
status: docs-checked
description: "Build a quality dashboard from CI and tracker data: test trends, flaky rate, coverage, escaped defects and lead time, with sources, refresh, and alert thresholds."
sources:
  - https://grafana.com/docs/grafana/latest/dashboards/
  - https://allurereport.org/docs/
  - https://dora.dev/guides/dora-metrics-four-keys/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quality dashboards

**Goal:** one always-current view of product and test health, so nobody compiles numbers by hand.

## Panels that earn their space
1. **Build health**: main branch pass/fail per day; time red.
2. **Test results trend**: passed/failed/skipped per run (Allure Report or JUnit XML aggregated).
3. **Flaky tests**: top 10 by flip rate, with owner.
4. **Suite duration**: p50/p95 pipeline time; alerts when over budget.
5. **Coverage**: line/branch trend and diff coverage per PR.
6. **Defects**: open by severity and component; created vs resolved burn-up.
7. **Escaped defects**: production defects per release by severity.
8. **Delivery**: deployment frequency, change failure rate, lead time.

## Data plumbing
- CI publishes JUnit XML -> parser job -> a database or metrics store.
- Tracker (Jira) via API or export job: one query per panel.
- Coverage from your coverage service's API.
- Grafana dashboards are sets of panels arranged in rows or tabs; keep the dashboard definition in git.

## Design
- Top row = the 3-4 numbers that decide release health; detail below.
- Each panel: definition tooltip, data source, refresh time.
- Thresholds coloured with agreed targets (e.g. a flaky-test rate target).
- Link panels to the drill-down (failing test history, Jira filter).

## Gotchas
- Stale dashboards destroy trust; show "last updated" and alert on ingestion failure.
- Mixing branches pollutes trends; filter to main.
- Too many panels; if nobody acted on a panel in a quarter, remove it.

## Verify
Dashboard is fed automatically, every panel has a definition and owner, and a team decision in the last month can be traced to it.

## Checked

2026-10-28 Confirmed against: Grafana docs (a dashboard is a set of panels arranged in rows or tabs); Allure Report docs (framework-agnostic test result visualisation, JUnit and other frameworks); DORA guide (deployment frequency, change fail rate, lead time). Removed or generalised: the vendor list (Allure TestOps, ReportPortal, Datadog, Buildkite, Codecov, SonarQube), the JQL example with a 90-day window, the Postgres/Prometheus claim, and the 1% flaky threshold (not sourced).

Method: documentation only; no commands were run.
