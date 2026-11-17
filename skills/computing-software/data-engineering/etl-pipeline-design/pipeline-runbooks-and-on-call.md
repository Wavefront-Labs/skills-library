---
id: computing-software.data-engineering.etl-pipeline-design.pipeline-runbooks-and-on-call
name: pipeline-runbooks-and-on-call
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, error-handling, pipeline-runbook, data-on-call, incident-response, severity-levels, alert-routing, postmortem, sla]
level: practitioner
status: draft
description: "Run data pipelines on call: tiering by business impact, alert routing, runbook template per pipeline, triage steps, stakeholder comms, handover and blameless postmortems."
sources:
  - https://sre.google/sre-book/being-on-call/
  - https://sre.google/workbook/on-call/
  - https://sre.google/sre-book/postmortem-culture/
  - https://response.pagerduty.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pipeline runbooks and data on-call

**Goal:** when a pipeline breaks at 3 a.m., whoever is on call can tell whether it matters, what to do, and who to tell — in minutes, from a document.

## 1. Tier pipelines by impact
| Tier | Example | Response |
|---|---|---|
| P1 | regulatory reporting, revenue feeding customer-facing product, billing | page 24/7, respond 15 min |
| P2 | exec dashboards with a morning SLA | page in business hours / before SLA, respond 1 h |
| P3 | exploratory, internal analytics | ticket, next business day |
Tier lives in metadata (dbt `meta.tier`, job tags) so alert routing reads it automatically.

## 2. Alert routing
- P1 → pager (PagerDuty/Opsgenie); P2 → pager during hours + channel; P3 → channel/ticket.
- One alert per incident: group task failures by pipeline/run; suppress downstream "missing data" alerts when the upstream failure is known.
- Every alert message contains: pipeline, failing step, error excerpt, run link, **runbook link**, owner, tier.

## 3. Runbook template (one per pipeline)
```
# <pipeline name>  (tier P2, owner: @team-sales-data, SLA: tables fresh by 07:00 UTC)
What it does: sources → outputs, consumers (dashboards, reverse ETL, partners)
Dependencies: upstream jobs / source systems + their support contacts
Common failures:
  - Source API 429/5xx → wait and repair-run task `extract` (safe: idempotent)
  - Partner file missing → check SFTP; email partner contact; mark SLA at risk
  - Duplicate key test fails → see quarantine table X; do NOT disable test; escalate to owner
How to rerun: exact command / UI steps, parameters (run_date), what's safe to rerun
How to backfill: command + max safe range
Who to tell: channel #sales-data-status, stakeholder list for SLA misses
Escalation: owner on-call → data platform → source system team
```
Test runbooks: a new team member should resolve a staged failure using only the runbook.

## 4. During an incident
1. Acknowledge; post in the status channel: impact, affected tables/dashboards, ETA unknown/known.
2. Stop the bleeding: pause downstream publishes (reverse ETL, partner exports) if bad data could propagate.
3. Diagnose with lineage (what changed: code deploy, source schema, volume).
4. Fix or work around; rerun/backfill; verify with data tests.
5. All-clear message with what was affected and whether numbers changed.

## 5. Rotation health
- Weekly rotation, handover notes (open issues, flaky jobs), follow-the-sun if teams allow.
- Track pages per shift; >2 actionable pages per shift or any non-actionable page → fix the alert or the pipeline.
- Blameless postmortem for P1 and repeated P2 incidents: timeline, impact, root cause, action items with owners and dates.

## Verify
- [ ] Every P1/P2 pipeline has a runbook linked from its alerts.
- [ ] Alert messages include owner, tier and run link.
- [ ] Pager load per shift is measured and reviewed monthly.
