---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.retiring-unused-and-ignored-alerts
name: retiring-unused-and-ignored-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alert-retirement, unused-alerts, alert-fatigue, alert-review-process, alerting-rules]
level: practitioner
status: docs-checked
description: "Identify alerts that never fire, always fire, or are always ignored, and retire or rework them through a regular review using the ALERTS series and pager history."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://sre.google/workbook/monitoring/", "https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retiring unused and ignored alerts

## What the sources say
- SRE Book (monitoring distributed systems): data collection, aggregation and alerting configuration that is rarely
  exercised (the book's example: less than once a quarter for some SRE teams) should be up for removal; signals that are
  collected but appear in no dashboard and no alert are candidates for removal; every page should be actionable; rules
  for humans should be simple and represent a clear failure.
- SRE Workbook: tying alerts directly to SLOs made them more clearly actionable and the false-positive rate decreased
  significantly in the case study; classify alerts by severity so responses are proportional (ticket versus page).
- Prometheus: for pending and firing alerts Prometheus stores a synthetic series
  `ALERTS{alertname="<alert name>", alertstate="<pending or firing>", ...}` with value 1 while the alert is in that
  state, marked stale afterwards. The "Alerts" tab of the Prometheus UI shows currently active alerts.

## Classify every rule at a regular review
| Category | Evidence to gather | Action |
|---|---|---|
| Never fired in the review window | `ALERTS` history for that `alertname` in your long-term store (Prometheus itself only keeps its retention) | confirm the expression still returns data, then keep, rework or delete |
| Always firing | `ALERTS` showing the alert active for long stretches | fix or delete: it trains people to ignore alerts |
| Fired, never acted on | pager acknowledgements without follow-up, postmortem notes | downgrade to ticket or dashboard, or delete |
| Duplicates another alert | fires on the same incidents | consolidate, keep the symptom-based alert |
| Useful | led to action | keep, check the runbook |

## Process
1. Export an inventory to a sheet: rule, owner, last fired, fires per review period, how often it was actioned.
2. The owner decides keep, rework or delete within an agreed period; unowned rules default to delete after notice.
3. Delete via a pull request referencing the review; Git keeps the history.

## Gotchas
- "Never fired" can mean broken, for example a renamed metric. Check the alert expression still returns data before
  calling it unused.
- Compliance-required alerts (backups, certificate expiry) stay even when quiet; mark them.

## Verify
- [ ] The review is recorded each period and the number of rules and pages per week is flat or falling.

## Checked

Checked 2026-11-08 against the SRE Book chapter, the SRE Workbook monitoring chapter and the Prometheus alerting rules
page. Removed because the cited pages do not state them: the 6-12 month and 90d windows, the `ALERTS_FOR_STATE` and
`/api/v1/rules` mechanics, the `absent()` check, Grafana state history, the two-week decision period and the "unit test"
step. The process table is workflow advice rather than quoted claims.
Method: docs-only read of cited pages, 2026-11-08
