---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.budget-reforecast
name: budget-reforecast
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, budgeting, budget-reforecast, reforecast, holdback, variance-analysis]
level: practitioner
status: docs-checked
description: "Update budgets from refreshed cloud forecasts: forecast vs budget variance, holdback use and reclaim, out-of-cycle adjustments, forecast drift rate."
sources: ["https://www.finops.org/framework/capabilities/budgeting/", "https://www.finops.org/framework/capabilities/forecasting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Budget reforecast and adjustment

Per the FinOps Framework, forecasts are the baseline for budgets, and a budget cadence should include
rolling forecasts that update budgets from business drivers.

## Steps
1. Refresh each owner's forecast model (history, planned changes, new features, architecture changes, optimisation work).
2. Compare forecast with budget using the Framework KPI: (budgeted effective cost minus forecast effective cost) divided by budgeted effective cost, on discount-adjusted amortised data.
3. Where a forecast will exceed budget, the forecast model owner seeks extra funding from the budget owner, and Engineering and Product investigate the cause. Optimise, or use holdback, or escalate to a higher budget owner, Finance and Leadership.
4. Where spend is strongly favourable to budget, the budget owner and Finance reclaim holdback that is no longer needed and redeploy it.
5. Use the agreed out-of-cycle adjustment process for any change, and record overrides, exceptions and service impacts.
6. Track Forecast Drift Rate (new forecast minus previous forecast, divided by previous forecast) to see how forecasts move over time.
7. Procurement watches budgets against actuals where an overrun would affect commitments or vendor agreements.

## Gotchas
- Budget is the organisation's funding commitment; a forecast is the owner's commitment to deliver value for a spend. Keep the two documents separate.
- A shorter budgeting cycle makes out-of-cycle changes routine and lets undesignated holdback be released.

## Verify
- [ ] Each budget owner has a refreshed forecast and a recorded budget decision.
- [ ] Out-of-cycle changes and holdback movements are logged.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Budgeting and Forecasting capability pages (full text read).
Removed as unconfirmed: mid-year timing, variance split categories, funded-growth rules, transfer log fields and the enterprise-commit shortfall advice.
