---
id: computing-software.cloud-infrastructure-engineering.observability.symptoms-vs-causes-monitoring
name: symptoms-vs-causes-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [symptoms-vs-causes, cause-based-dashboards, symptom-based-alerting, alert-design, golden-signals]
level: practitioner
status: docs-checked
description: "Page on symptoms (what is broken for users) and use causes (why) for debugging and tickets; routing tiers and a migration plan for cause-based alerts."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://sre.google/sre-book/practical-alerting/", "https://sre.google/workbook/alerting-on-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Symptoms vs causes

The SRE book says monitoring should answer what is broken (the symptom) and why (the possibly intermediate cause). One team's symptom can be another's cause: slow database reads are a symptom for the database SRE and a cause for the frontend SRE. Black-box monitoring suits paging because it alerts only when users are already affected; white-box monitoring is essential for debugging.

## Routing (Practical Alerting chapter)
- Page-worthy alerts go to the on-call rotation.
- Important but subcritical alerts go to ticket queues.
- Everything else is kept as informational data for status dashboards.
- White-box monitoring can only alert on failures you expected; failures that never reach the target (for example DNS errors) need black-box probes.

## Illustrative mapping (author's examples, not from the pages)
| Symptom (page) | Causes (dashboard or ticket) |
|---|---|
| Error ratio burning SLO budget | database connection errors, pod restarts, upstream 5xx |
| Latency over SLO | CPU throttling, pauses, cache hit ratio drop |
| Users cannot log in (probe fails) | identity provider errors, certificate expiry, DNS |

The Workbook's SLO burn-rate alerts are the recommended way to page on a threat to the error budget instead of on individual internal metrics.

## Migrating cause-based alerts (practice advice)
1. Export all rules and tag each symptom or cause.
2. For each cause alert, make sure a symptom alert covers what it tried to catch.
3. Demote the cause alert to a ticket or dashboard panel and link it from the symptom's runbook.
4. Track pages per week before and after.

## Dashboards
Put symptoms (SLIs) first, then cause panels in the order you would check them.

## Gotcha
Removing a cause alert before a symptom alert covers it creates a blind spot.

## Verify
- [ ] Each paging rule maps to a user-visible symptom or an SLO burn
- [ ] Each symptom alert's runbook lists the cause panels to check

## Checked

2026-11-08. Confirmed in the SRE book monitoring chapter: symptom/cause definitions, the DB example, black-box for paging, white-box for debugging. Confirmed in Practical Alerting: routing tiers and white-box limits; that chapter does not discuss symptoms versus causes itself (footnote only). The Workbook SLO alerting chapter supports burn-rate paging. Removed: the thresholds for cause pages (disk full in 4 h, certificate under 7 days), and the "high CPU at 3am" claim, since none of the pages state them. The mapping table and migration steps are marked as practice advice.
Method: documentation only; no commands were run.
