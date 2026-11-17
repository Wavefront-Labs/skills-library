---
id: computing-software.cloud-infrastructure-engineering.observability.alert-noise-review-and-consolidation
name: alert-noise-review-and-consolidation
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [alerting, alert-fatigue, alert-noise-metrics, alerts-per-shift, alert-review-process, weekly-alert-review, alert-consolidation, alert-dedup-rules, inhibit-rules]
level: practitioner
status: draft
description: "Measure alert noise (pages per shift, actionable ratio) from Alertmanager data, run a weekly alert review, and consolidate duplicate rules with inhibition and grouping."
sources: ["https://sre.google/workbook/on-call/", "https://sre.google/sre-book/practical-alerting/", "https://prometheus.io/docs/alerting/latest/configuration/#inhibit_rule"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alert noise review and consolidation

## Measure
```promql
# Notifications sent per integration per day (Alertmanager self-metrics)
sum by (integration) (increase(alertmanager_notifications_total[1d]))
# Distinct alerts firing per day, by alertname (Prometheus ALERTS series)
count by (alertname) (count_over_time(ALERTS{alertstate="firing", severity="page"}[1d]))
# Flapping: alerts that changed state many times
sort_desc(sum by (alertname) (changes(ALERTS_FOR_STATE[1d])))
```
From the paging tool (PagerDuty/Grafana OnCall/Opsgenie) export incidents per shift and tag each with
**actionable? (y/n)** and **action taken**. Targets from the SRE Workbook: at most ~2 incidents per 12 h shift;
aim for > 50 % actionable, and treat anything below as a project.

## Weekly alert review (30 min, on-call + owner)
1. List every page from the past week (export).
2. For each: real user impact? action taken? would a ticket have sufficed? duplicate of another page?
3. Decide: keep, tune threshold/`for`, demote to ticket, delete, automate the fix.
4. Track decisions as tickets; re-check the counts next week.
Keep the review blameless: noisy alerts are a system property.

## Consolidate
- **One symptom, one page**: if `APIHighLatency` and `APIHighErrorRate` and five cause alerts fire together,
  page on the SLO burn alert and demote the rest to ticket/info.
- **Inhibit** downstream noise:
```yaml
inhibit_rules:
  - source_matchers: [alertname="ClusterUnreachable"]
    target_matchers: [severity=~"page|ticket"]
    equal: [cluster]
  - source_matchers: [severity="page"]
    target_matchers: [severity="ticket"]
    equal: [alertname, namespace]
```
- **Group** related alerts in one notification: `group_by: [alertname, cluster, namespace]`, not `[...]` (all labels).
- Merge threshold variants (`DiskFull80`, `DiskFull90`, `DiskFull95`) into one rule with severity tiers or a
  `predict_linear` "fills within N hours" rule.

## Verify
- [ ] Pages per shift and actionable ratio charted weekly.
- [ ] Each alert deleted or demoted has a linked review note.
