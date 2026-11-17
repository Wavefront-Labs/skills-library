---
id: computing-software.qa-testing-engineering.test-case-design.defect-density-age-and-reopen-metrics
name: defect-density-age-and-reopen-metrics
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [defect-age, defect-density, reopen-rate, defect-metrics, defect-management]
level: practitioner
status: docs-checked
description: "Compute and use defect metrics: density per size, age and time-in-status, reopen rate, fix turnaround and containment, with JQL and pitfalls of gaming."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
  - https://support.atlassian.com/jira-software-cloud/docs/jql-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defect metrics: density, age, reopen rate

**Goal:** a small set of defect metrics that reveal quality and process problems without turning into targets people game.

## Metrics
- **Defect density** = defects found / size (KLOC, function points, or story points) per component or release. Compare components within one product, not across teams.
- **Defect age** = now (or resolved date) - created date. Report median and 90th percentile open age by severity. Old high-severity defects are a risk signal.
- **Time in status:** waiting for triage, in fix, waiting for retest. Shows where flow stalls (often retest or triage).
- **Reopen rate** = defects reopened at least once / defects resolved. A rising rate suggests weak fixes, vague reports or poor retests.
- **Fix turnaround** by severity vs agreed SLA (e.g. critical < 1 day).
- **Defect containment / escape rate** = found before release / total including production.
- **Rejected rate** (not a bug, duplicate, cannot reproduce): high values point at report quality or unclear requirements.

## Jira queries
Build saved JQL filters for open high-priority bugs older than N days and for bugs whose status changed to reopened (Atlassian documents the `CHANGED` operator). Age and time-in-status: use Jira's built-in reports or export the issue history.

## Pitfalls
- Counting defects per tester or developer destroys reporting honesty.
- Density depends on test effort; normalise or note it.
- Use trends and distributions, not single numbers.

## Verify
The metric set is defined with formulas in the test strategy, reproduced from saved queries, and reviewed monthly with actions attached to outliers.

## Checked

2026-10-28. Confirmed: Atlassian JQL functions page lists the CHANGED operator. Removed: The two JQL queries (DURING, priority and resolution syntax unconfirmed), the 5-10% reopen threshold and Jira report/REST specifics.

Method: documentation only; no commands were run.
