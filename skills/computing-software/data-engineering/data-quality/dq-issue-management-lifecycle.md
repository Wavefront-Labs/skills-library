---
id: computing-software.data-engineering.data-quality.dq-issue-management-lifecycle
name: dq-issue-management-lifecycle
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, dq-issue-management, dq-dimensions, issue-triage, root-cause, data-incident, remediation, dmbok, issue-log]
level: practitioner
status: draft
description: "Run a data quality issue lifecycle: logging issues with dimension and impact, triage and severity, assignment to data owners, root cause, remediation vs prevention, closure and trend reporting."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://www.iso.org/standard/35736.html
  - https://sre.google/sre-book/postmortem-culture/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data quality issue management lifecycle

**Goal:** every data quality problem — found by a test, a monitor or a business user — is recorded, owned, fixed at the root and learned from, instead of being patched silently in a dashboard.

## 1. One intake, one log
Sources of issues: failing tests/monitors, user reports, reconciliation breaks, audit findings. Route all into one tracker (Jira project, ServiceNow queue, or a DQ tool's incident module) with a form:
| Field | Example |
|---|---|
| Dataset / column | `gold.revenue_daily.net_amount` |
| Dimension | completeness / validity / accuracy / consistency / timeliness / uniqueness |
| Description + evidence | query, sample rows, screenshot |
| Detected by / when | monitor `rev_null_rate`, 2026-10-16 06:10 |
| Business impact | finance close dashboard wrong for EU |
| Severity | S1-S4 |
| Owner | data owner of the domain (business) + technical assignee |

## 2. Severity matrix
| | Critical data element / regulated | Important | Low use |
|---|---|---|---|
| Wrong numbers published | S1 | S2 | S3 |
| Delayed / incomplete | S2 | S3 | S4 |
| Cosmetic / documentation | S4 | S4 | S4 |
S1/S2 follow incident handling (on-call, status updates, see pipeline runbooks); S3/S4 go to the backlog with an SLA (e.g. S3: 10 business days).

## 3. Lifecycle states
`New → Triaged (severity, owner) → Investigating → Root cause identified → Remediating → Verified → Closed` (plus `Won't fix / accepted risk` with a documented approver).
- **Containment first** for S1/S2: stop propagation (pause exports, flag dashboards), then fix.
- **Correction** (repair the bad data: backfill, restatement) and **prevention** (fix the cause: source validation, contract, test) are separate tasks — an issue isn't closed until prevention is done or explicitly declined.

## 4. Root cause categories
Track a category per issue to see patterns: source system defect, manual data entry, upstream schema change, pipeline code bug, reference data missing, late data, requirement misunderstanding, tooling/infra. Recurring categories point to systemic fixes (data contracts for schema changes, entry validation in the source app).

## 5. Report and improve
Monthly: open issues by severity and age, MTTD/MTTR, issues per dataset and per root cause, % detected by automation vs users (target: automation finds most). Feed results into the DQ scorecard and the stewardship forum.

## Verify
- [ ] Every failing S1/S2 alert produces a ticket automatically.
- [ ] Each closed issue has root cause category and a prevention action or accepted-risk sign-off.
- [ ] Ageing report reviewed by data owners monthly.
