---
id: computing-software.qa-testing-engineering.test-case-design.change-failure-rate-and-escaped-defects
name: change-failure-rate-and-escaped-defects
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [change-failure-rate, escaped-defects, dora-metrics, quality-signals, defect-escape-rate]
level: practitioner
status: docs-checked
description: "Use DORA change failure rate and escaped defects as quality signals: definitions, data sources, calculating them per service, and acting on the trend."
sources:
  - https://dora.dev/guides/dora-metrics-four-keys/
  - https://dora.dev/research/
  - https://github.com/dora-team/fourkeys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change failure rate and escaped defects as quality signals

**Goal:** measure test effectiveness by outcomes in production, not by test activity.

## Change failure rate (DORA)
DORA describes change fail rate as the ratio of deployments that require immediate intervention following a deployment, likely resulting in a rollback or a hotfix (dora.dev DORA metrics guide).
```
CFR = deployments that caused an incident or required remediation / total deployments
```
- Data: deployment events (CI/CD), incidents (your incident tracker) or hotfix PRs linked to the deploy that caused them.
- DORA's four keys project (`dora-team/fourkeys`) shows a reference pipeline.
- Pair with failed deployment recovery time (DORA's current name for what was MTTR) and deployment rework rate (unplanned deployments that happen as a result of an incident in production).

## Escaped defects
- Any defect found in production (by users, monitoring, support) that existed in a released version.
- Tag in the tracker: `found-in: production`, `introduced-in: <release>`, `should-have-been-caught-at: unit|integration|e2e|review|none`.
- Report per release and per service, weighted by severity.

## Using them
- Rising CFR on a service -> look at its test gaps (which level would have caught the failures?), deployment size, and review practices.
- Escape analysis each sprint: for each escaped defect, add the missing test at the lowest level that would catch it.
- Contrast with deploy frequency: lowering CFR by deploying less often is not improvement.

## Gotchas
- Definitions must be agreed (does a feature-flag rollback count? decide and write it down).
- Small numbers per month are noisy; use rolling windows.
- Incidents not linked to deployments make CFR undercount; enforce the link in the incident template.

## Verify
CFR and escaped defects are computed automatically per service, definitions are written down, and each escaped defect has a linked follow-up test.

## Checked

2026-10-28 Confirmed against: dora.dev DORA metrics guide (change fail rate definition, failed deployment recovery time replacing MTTR, deployment rework rate, deployment frequency); dora-team/fourkeys repository (collects data from GitHub or GitLab to compute the four keys). Removed or generalised: the verbatim quotation (the definition above is paraphrased from the page), PagerDuty/Opsgenie names, the feature-flag verdict, and the 90-day window (not sourced).

Method: documentation only; no commands were run.
