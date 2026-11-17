---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.driver-based-forecasting
name: driver-based-forecasting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-forecasting, driver-based-forecasting, business-drivers, unit-cost-forecast]
level: advanced
status: docs-checked
description: "Where driver-based forecasting fits in the FinOps Forecasting capability: Run-level model mix, business drivers, and unit economics as the link."
sources: ["https://www.finops.org/framework/capabilities/forecasting/", "https://www.finops.org/framework/capabilities/unit-economics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Driver-based forecasting

The Forecasting capability describes Run-level forecast models as a combination of rolling,
trend-based and driver-based. It also lists forecast frequency that includes intermediate forecasts
to update budgets based on business drivers.

## Steps
1. Choose business drivers that explain usage for the service or product. Unit metrics from the Unit Economics capability (cost per transaction, customer, GB, token) give the cost per driver, and the usage counter is the driver.
2. Get driver expectations from the business, with Product, Leadership and Finance input, so forecasts reflect planned demand.
3. Combine with rolling and trend-based models rather than using drivers alone.
4. Base forecasts on discount-adjusted, amortised usage and include usage optimisation opportunities.
5. Align forecast granularity to the organisation's allocation constructs (business unit, cost center, team, product, service).
6. Issue intermediate forecasts when drivers change, and review thresholds and trends with stakeholders on a regular cadence.

## Verify
- [ ] Drivers and their cost-per-driver metrics are documented per forecast.
- [ ] Forecast variance is tracked (see forecast-accuracy).

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Forecasting and Unit Economics capability pages (full text read).
Removed as unconfirmed: the regression of cost on driver, the 6-12 months history and R-squared check, the driver list, step-cost advice, base/high/low scenarios, monthly reconcile and quarterly coefficient refresh, the savings haircut, and the top-10 service verify items.
