---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.error-budgets
name: error-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, management-and-monitoring, error-budgets, slo, burn-rate-alerts, multiwindow-alerting, error-budget-policy, sre]
level: practitioner
status: draft
description: "Implement SLO error budgets: SLI definitions, budget calculation, multi-window burn-rate alerts, and an error budget policy that changes release behaviour when budgets run out."
sources: ["https://sre.google/workbook/implementing-slos/", "https://sre.google/workbook/alerting-on-slos/", "https://sre.google/workbook/error-budget-policy/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SLO alerting with error budgets

## Basics
- SLI = good events / valid events (e.g. requests < 300 ms and non-5xx / all requests).
- SLO = target over a window (99.9% over 28 days).
- **Error budget** = 1 - SLO = 0.1% of requests (~40 minutes of full outage per 28 days).

## Burn-rate alerting (Google SRE workbook)
Burn rate = observed error rate / budgeted error rate. Recommended multiwindow, multi-burn-rate:
| Severity | Burn rate | Long window | Short window | Budget consumed |
|---|---|---|---|---|
| Page | 14.4 | 1 h | 5 min | 2% in 1 h |
| Page | 6 | 6 h | 30 min | 5% in 6 h |
| Ticket | 1 | 3 days | 6 h | 10% in 3 days |
Alert when both long and short windows exceed the burn rate (short window gives fast reset).

PromQL sketch:
```
(sum(rate(http_requests_total{code=~"5.."}[1h])) / sum(rate(http_requests_total[1h]))) > (14.4 * 0.001)
and
(sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) > (14.4 * 0.001)
```

## Error budget policy
Agreed in advance by product and engineering: when the budget is exhausted, freeze non-critical
releases, prioritise reliability work, require postmortems for budget-consuming incidents; resume
when back within budget.

## Gotchas
- SLOs at 100% or copied from provider SLAs; pick targets users need.
- Low-traffic services: a few failures blow the budget; use longer windows or synthetic traffic.

## Verify
- [ ] Each tier-1 service has SLOs, dashboards and burn-rate alerts.
- [ ] Policy signed by product owner and used at least once.
