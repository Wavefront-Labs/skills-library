---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.error-budget-exhaustion-ticket-alerts
name: error-budget-exhaustion-ticket-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [budget-exhaustion-alert, slow-burn-ticket, error-budget, slo-based-alerting, error-budget-policy]
level: practitioner
status: docs-checked
description: "Ticket-severity SLO alerts per the Google SRE Workbook: the 10% budget in 3 days slow burn, multiwindow burn-rate rules, and how the error budget policy follows."
sources: ["https://sre.google/workbook/alerting-on-slos/", "https://sre.google/workbook/error-budget-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error budget ticket alerts

Pages are for fast burns; a slower signal catches errors that "typically go unnoticed but can exhaust your error budget if left unchecked". The SRE Workbook sends those as tickets, not pages (pages and tickets are the only valid ways to get a human to act).

## Definitions (Workbook and example policy)
- Error budget = 1 minus the SLO; a 99.9% SLO has a 0.1% budget.
- Burn rate 1 means consuming budget at a rate that leaves exactly 0 at the end of the SLO window (99.9% over 30 days: a constant 0.1% error rate).
- Budget consumed = burn rate x alert window / SLO period.

## Recommended thresholds (Table 5-6 and 5-8, 99.9% SLO over 30 days)
| Severity | Long window | Short window | Burn rate | Budget consumed |
|---|---|---|---|---|
| Page | 1 hour | 5 minutes | 14.4 | 2% |
| Page | 6 hours | 30 minutes | 6 | 5% |
| Ticket | 3 days | 6 hours | 1 | 10% |
The Workbook calls 10% in three days "a good baseline for ticket alerts" and says the numbers depend on the service and baseline page load; for busier services you may want ticket alerts on the six-hour window. Make the short window about 1/12 of the long window.

## Rule shape from the Workbook
Prerequisite: recording rules for the error ratio over each window (the Workbook uses `job:slo_errors_per_request:ratio_rate<window>`). Ticket alerts (as printed in the Workbook, 0.001 = 1 - SLO):
```yaml
expr: (
        job:slo_errors_per_request:ratio_rate24h{job="myjob"} > (3*0.001)
      and
        job:slo_errors_per_request:ratio_rate2h{job="myjob"} > (3*0.001)
      )
    or
      (
        job:slo_errors_per_request:ratio_rate3d{job="myjob"} > 0.001
      and
        job:slo_errors_per_request:ratio_rate6h{job="myjob"} > 0.001
      )
severity: ticket
```
Notes from the page: a `for:` duration is not a good substitute for long windows (a series of 5-minute 100% error spikes every 10 minutes never fires a 10-minute `for` alert while consuming 35% of the budget); with several burn-rate alerts you need suppression so one incident does not open three notifications; the 3-day window has a long reset time; if an issue will exhaust the budget within hours or a few days, an active notification is appropriate, otherwise a ticket to address next working day.

## Error budget policy
The Workbook's example policy: when the service has exceeded its error budget for the preceding four-week window, halt all changes and releases other than P01 issues or security fixes until the service is back within its SLO; if a single incident consumes more than 20% of the budget over four weeks, a postmortem with at least one P0 action item is required. These are example values from a sample document, to be agreed with the product owner. Routing ticket alerts to the policy owners rather than the pager follows from the Workbook's page-or-ticket split.

## Verify
- [ ] The ticket alert fires on a replayed slow burn near burn rate 1 and does not fire on a short spike.
- [ ] The alert's severity label routes it to the ticket queue, not the pager.

## Checked
Date: 2026-11-07. Read: the SRE Workbook "Alerting on SLOs" page (burn-rate definition, iterations 5 and 6, Tables 5-6 and 5-8, the pros/cons and `for:` discussion; the low-traffic and "alerting at scale" sections were skimmed only) and the "Example Error Budget Policy" appendix in full. Thin skill: the draft's core idea, recording a "remaining budget" ratio over 28 days and alerting when it drops below 25% or reaches 0, is not described on either page, so those rules, the 28d increase query, the 5-15m evaluation interval, the Thanos/Mimir retention advice, the 24h `repeat_interval` advice and the recovery-date gotcha were removed and the skill was rewritten around the Workbook's ticket-alert recipe. The Prometheus functions page was dropped from sources (not read). Description reworded to match.
Method: documentation only; no commands were run.
