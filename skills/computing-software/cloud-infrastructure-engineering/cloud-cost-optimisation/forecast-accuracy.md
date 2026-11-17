---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.forecast-accuracy
name: forecast-accuracy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-forecasting, forecast-accuracy, forecast-variance, forecast-drift, variance-thresholds]
level: practitioner
status: docs-checked
description: "Measure forecast accuracy with the FinOps Framework KPIs: spend and usage accuracy rate, drift rate, agreed variance thresholds and what to do on a miss."
sources: ["https://www.finops.org/framework/capabilities/forecasting/", "https://www.finops.org/framework/maturity-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forecast accuracy tracking

## Framework KPIs
- **Forecast Accuracy Rate (Spend)**: (forecasted spend minus actual spend) divided by forecasted spend, over a period such as day, month or quarter. Percentage variance is the primary metric; dollar differences are also informative.
- **Forecast Accuracy Rate (Usage)**: the same ratio for usage, measured per service type (service name, SKU, service category or sub-category).
- **Forecast Drift Rate**: (new forecast minus previous forecast) divided by previous forecast, showing how forecasts change over time from priority shifts, workload changes, rightsizing and commitment discounts.
- Each organisation defines its own acceptable variance, expressed as an agreed maximum variance from actual spend.
- The Maturity Model page lists sample community goals for forecast-to-actual accuracy variance: below 20% at Crawl, below 10% at Walk, below 5% at Run. These are general guidelines, not targets to reach everywhere.

## Steps
1. Use discount-adjusted, amortised usage data for forecasts and for the comparison.
2. Agree variance thresholds with Product, Finance and Leadership.
3. Notify stakeholders when the forecast variance threshold is exceeded and a budget overspend is at risk.
4. Compare projected avoidance with observed outcomes and feed lessons into standards and later estimates.
5. At Run maturity the Framework expects granular visibility (by business unit, cost centre, team, product, service) rather than only aggregate forecasting.

## Gotchas
- Forecast quality depends on allocation: costs must be fully categorised and allocated before forecasts by team are reliable.
- The 20, 15 and 12 percent variance figures (Crawl, Walk, Run) in the Budgeting capability apply to budget vs actual spend, not to forecast accuracy.

## Verify
- [ ] Accuracy rate and drift rate are reported per forecast owner.
- [ ] Threshold breaches trigger a stakeholder notification.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Forecasting and Budgeting capability pages and Maturity Model pages (full text read).
Removed as unconfirmed: MAPE and bias definitions, the attribution of 20/15/12 percent thresholds to forecasts (they belong to budgets), snapshot/versioning steps and the monthly/quarterly cadence.
