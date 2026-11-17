---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.new-workload-forecast
name: new-workload-forecast
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, forecasting, new-workload-forecast, ramp-curve, cost-estimation, migration-forecast, launch-planning]
level: practitioner
status: docs-checked
description: "Forecast new workloads with no history: turn an estimate into a forecast model with timing, pricing and TCO, then revisit against early actuals."
sources: ["https://www.finops.org/framework/capabilities/forecasting/", "https://www.finops.org/framework/capabilities/planning-estimating/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forecasting new workloads without history

The FinOps Framework says forecasts are usually based on estimating, which looks at historical
spend, future plans, and how lifecycle changes will affect usage. For a new workload there is
no history, so the estimate is the starting point and the forecast model adds timing.

## Steps
1. **Start from the estimate** produced under Planning and Estimating (see
   `load-based-estimation`). Engineering drives it; the forecasting strategy vets it against
   current baseline forecasts or establishes a new model to feed Budgeting.
2. **Document timing and implementation**: the forecast model records when each part of the
   system is implemented, the pricing models used and when they take effect, and the total cost
   of ownership of the scope.
3. **Phase the environments**: the page's example is development and test launched first and
   production months later, rather than all environments from day one.
4. **Include rate optimisation** once the forecast matures (Walk maturity includes commitment
   discounts) and optimisation opportunities at Run.
5. **Agree the model** between Engineering and Product with Finance and Leadership consulted.
   Once agreed, the budget owner must meet the forecast or seek variance funding.
6. **Revisit at a defined point** such as go-live, comparing the original estimate to early
   actuals, and feed the variance back into the estimating method.
7. **Keep the model current** as the system is operated and modified; owners adjust it over time.

## Verify
- [ ] The new workload has a forecast model with timing, pricing and ownership.
- [ ] A revisit point is set and the estimate-versus-actual variance is recorded.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Forecasting and Planning and Estimating capability pages (Forecasting read through the functional activities, Planning and Estimating through the maturity levels). The Onboarding Workloads page returned 404 and was dropped. Removed unconfirmed: the dev/test and production ramp percentages, migration waves and double running, the worked $40k ramp table, 2-3 month and 6 month switch points, the separate "new initiatives" line and the gotchas.
