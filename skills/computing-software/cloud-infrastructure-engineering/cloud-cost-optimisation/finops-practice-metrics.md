---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-practice-metrics
name: finops-practice-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-practice-operations, finops-practice, finops-practice-metrics, practice-health-scorecard]
level: practitioner
status: draft
description: "Measure the health of the FinOps practice itself: visibility, forecast, rate, usage, anomaly and engagement metrics with formulas, targets and a monthly scorecard."
sources: ["https://www.finops.org/framework/capabilities/finops-practice-operations/", "https://www.finops.org/wg/finops-kpis/", "https://www.finops.org/framework/maturity-model/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FinOps practice health metrics

Separate from business KPIs such as unit cost, these tell you whether the practice is working.

## Metric set (pick 8-10)
| Area | Metric | Typical target |
|---|---|---|
| Visibility | % of spend allocated to an owner (amortised) | >= 90-95% |
| Visibility | Cost data latency, usage to dashboard | < 48 h |
| Forecast | Monthly forecast variance per BU | within +/-10% (Run: +/-5%) |
| Rate | Effective savings rate (ESR) | rising; compare with peers |
| Rate | Commitment utilisation | >= 95% |
| Usage | Realised savings / identified savings | > 50% |
| Usage | Age of open optimisation tickets | median < 30 days |
| Anomaly | Mean time to detect / resolve | < 1 day / < 5 days |
| Engagement | Top spenders with an active budget and monthly review | 100% |
| Engagement | Monthly active engineer users of cost dashboards | rising |
| Policy | Tag compliance on new resources | >= 98% |

## Steps
1. Baseline each metric from current data before setting any target.
2. Write each formula down (amortised vs unblended, account scope) so trends stay comparable.
3. Automate collection from the cost warehouse and ticketing system; no manual spreadsheets.
4. Publish a monthly scorecard with trend arrows to the FinOps steering group.
5. Re-target yearly or after a maturity reassessment.

## Gotchas
- Counting "savings identified" rewards noise; report realised savings.
- Allocation % on unblended cost hides commitment purchases; use amortised.
- A 30-line scorecard nobody reads; keep it to one screen.

## Verify
- [ ] Each metric has a written formula, data source, owner and target.
- [ ] The scorecard regenerates automatically each month.
