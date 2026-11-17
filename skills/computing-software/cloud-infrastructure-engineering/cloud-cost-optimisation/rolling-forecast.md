---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rolling-forecast
name: rolling-forecast
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-forecasting, rolling-forecast, forecast-cadence, finance-partnership]
level: practitioner
status: docs-checked
description: "Run a rolling, trend-based cloud forecast with Finance, following the FinOps Forecasting capability: owners, inputs, review cadence and variance thresholds."
sources: ["https://www.finops.org/framework/capabilities/forecasting/", "https://www.finops.org/framework/capabilities/budgeting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling forecast with finance

## Where it fits in the maturity model
- Crawl: manual, ad hoc models based on historical spending.
- Walk: forecasts are rolling and trend-based, include rate optimisation and commitment discounts, are updated on a regular cadence (not automated), and are reviewed regularly by the FinOps team with stakeholders.
- Run: a combination of rolling, trend-based and driver-based models, including usage optimisation opportunities, on discount-adjusted amortised usage, with real-time visibility and automated flow to accounting systems.

## Steps
1. Agree a forecasting strategy with FinOps, Engineering, Product, Finance and Leadership: how often forecasts are due, the forecast length and the variance thresholds.
2. Engineering and Product owners build and maintain the forecast model for their systems, using history, planned changes, timing and pricing models to be used and when.
3. FinOps and Finance provide granular forecast reporting and budget vs actual vs forecast views to compare against variance KPIs.
4. Notify stakeholders when the agreed forecast variance threshold is exceeded and a budget overspend is at risk.
5. Where actual cost exceeds forecast (or is expected to), the model owner seeks additional funding from the budget owner.
6. Feed outcomes back: compare projected avoidance with observed results and feed lessons into future estimates.

## Gotchas
- Forecasting is a commitment by the owners; do not make it a FinOps-only artefact.
- Keep Estimating, Forecasting and Budgeting distinct even in small organisations where they happen together.

## Verify
- [ ] Each system has a named forecast owner and an agreed update cadence.
- [ ] Forecast variance KPIs (accuracy rate, drift rate) are reported.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Forecasting and Budgeting capability pages (full text read).
Removed as unconfirmed: the 12-18 month horizon, the monthly/quarterly/ad hoc cadence, the plus or minus 10 percent threshold, MAPE and the snapshot template (the Framework does not prescribe these).
