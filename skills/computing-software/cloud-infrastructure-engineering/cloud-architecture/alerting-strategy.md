---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.alerting-strategy
name: alerting-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, management-and-monitoring, management-baseline, alerting-strategy, actionable-alerts, symptom-based-alerting, alert-fatigue, paging-policy]
level: practitioner
status: docs-checked
description: "Design an alerting strategy: page only on user-impacting symptoms, route by ownership and severity, link runbooks, and prune noisy alerts with regular reviews."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://sre.google/workbook/alerting-on-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alerting strategy and actionable alerts

## Principles
- **Page on symptoms** that users feel (error rate, latency, availability SLO burn), not on every
  cause (CPU 80%). "What is broken" is the symptom, "why" is the cause; spend much more effort on catching
  symptoms, and for causes only alert on very definite, very imminent ones.
- Every page must be **actionable and urgent, needs intelligence, and concern a novel problem**; a page that merely
  merits a robotic response should not be a page, and one that could wait until morning is a ticket.
- Every alert has an **owner** and a **runbook link** (team practice, not from the cited pages).

## Severity and routing
The SRE book classifies human-directed notifications as tickets, email alerts and pages. Illustrative routing:

| Severity | Example | Route |
|---|---|---|
| Page | SLO fast burn, checkout down | On-call phone |
| Ticket | Slow SLO burn, disk forecast to fill in days | Team queue |
| Info | Deploy finished | Chat channel / none |

## Steps
1. List services and their SLOs; define burn-rate alerts first. Burn rate is how fast the service consumes error
   budget relative to the SLO (burn rate 1 uses exactly the whole budget by the end of the window). The SRE Workbook
   recommends multiple burn-rate windows: 2% of budget in 1 hour (burn rate 14.4) and 5% in 6 hours as reasonable
   starting points for paging, and 10% in 3 days as a baseline for tickets; tune to the service and page load.
2. Add a small set of cause-based alerts that predict outages with lead time (disk full forecast,
   certificate expiry, quota near limit).
3. Route via tags/labels to owning team rotation (PagerDuty/Opsgenie/action groups).
4. Template alert text: what, impact, where, dashboard, runbook.
5. Monthly alert review: pages per shift, % actionable, top noisy alerts -> fix or delete.

## Gotchas
- Thresholds copied from defaults; set based on SLOs and baselines.
- Alerts on every instance in an autoscaling group; alert on the aggregate.
- Missing "no data" handling: silent failures when metrics stop.

## Verify
- [ ] Pages per on-call shift within your agreed target; the SRE book notes people can react with urgency only a
  few times a day before becoming fatigued.
- [ ] 100% of paging alerts have runbooks.

## Checked
2026-11-08. Confirmed against the SRE book chapter Monitoring Distributed Systems (symptoms vs causes, the page
philosophy bullets, tickets/email/pages; read in the alerting sections) and the SRE Workbook chapter Alerting on
SLOs (burn rate definition, 2%/1 h and 5%/6 h paging, 10%/3 days ticket; read in the burn-rate sections). The cited
Azure Well-Architected alerting page returned 404, so it was dropped from sources. Removed the unsourced "less than 2
per 12 h shift" target and the Sev1/2 and 21-day certificate examples. Ownership, runbook links, aggregate-versus-
instance alerting and no-data handling are practice advice, not vendor claims.
Method: documentation only; no commands were run.
