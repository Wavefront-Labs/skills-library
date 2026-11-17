---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.rolling-vs-calendar-slo-windows
name: rolling-vs-calendar-slo-windows
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [rolling-window-slo, calendar-window-slo, slo, error-budget, slo-target-selection]
level: practitioner
status: docs-checked
description: "Pick rolling (e.g. four-week) or calendar-aligned (monthly, quarterly) SLO compliance windows and compute both in PromQL and reporting."
sources: ["https://sre.google/workbook/implementing-slos/", "https://sre.google/sre-book/service-level-objectives/", "https://prometheus.io/docs/prometheus/latest/querying/functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling vs calendar SLO windows

## Trade-off (SRE Workbook, Implementing SLOs)
- Rolling window: closer to user experience (an outage on the last day of a month is not forgotten on the first of the
  next). Use a whole number of weeks so every window holds the same number of weekends; a four-week rolling window is
  Google's general-purpose choice.
- Calendar window (e.g. quarter): closer to business planning and project work, but mid-period you cannot know how many
  requests the rest of the period will bring, so decisions speculate about remaining budget.
- Shorter windows support quick course corrections; longer ones suit strategic decisions.
Google complements the four-week rolling window with weekly summaries for task prioritisation and quarterly reports for
project planning.

## PromQL
```promql
# rolling 28d
sum(increase(slo:requests_good:count[28d])) / sum(increase(slo:requests_total:count[28d]))
```
`slo:...` are your own recording-rule names. For a calendar period, compute the range in the dashboard or reporting
tool and substitute it for `28d`.

## Budget arithmetic
Budget minutes = (1 - SLO) x window minutes. 99.9% over 28d = 40.3 min; over a 31-day month = 44.6 min; over a quarter (~91d) = 131 min.

## Gotchas
- `increase()` adjusts for counter resets such as target restarts, but aggregate after it: take `increase`/`rate`
  first, then `sum` (Prometheus function docs).

## Verify
- [ ] Rolling and calendar numbers are both on the SLO dashboard, labelled.
- [ ] Retention of the source data exceeds the longest window.

## Checked
2026-11-01. Confirmed in the SRE Workbook (Implementing SLOs): rolling vs calendar trade-offs, whole weeks, four-week
rolling window, weekly and quarterly complements; and the Prometheus function docs (`increase` counter-reset
handling, aggregate after rate). Budget minutes are arithmetic. Removed: Grafana time-range steps, retention flag
name, cost claim for `increase` over raw counters, "budget recovers gradually" wording.
Method: documentation only; no commands were run.
