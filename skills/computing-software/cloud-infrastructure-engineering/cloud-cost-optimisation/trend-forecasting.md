---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.trend-forecasting
name: trend-forecasting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-forecasting, trend-forecasting, run-rate, time-series-forecast, seasonality]
level: practitioner
status: docs-checked
description: "Produce a trend-based cloud cost forecast: clean amortised history, rolling and trend models, known changes, variance thresholds and when to add drivers."
sources: ["https://www.finops.org/framework/capabilities/forecasting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trend-based forecasting

The FinOps Framework places trend-based and rolling forecasts at the Walk stage and adds driver-based models at Run.
Use a trend forecast for steady workloads and add drivers where growth is planned.

## Steps
1. **Use discount-adjusted, amortised usage** as the forecast basis, at the granularity your allocation scheme
   supports (business unit, cost centre, team, product or service).
2. **Clean the history**: handle one-offs (commitment purchases in a billed view, incidents, migration double-running,
   credits) by removing them or modelling them separately.
3. **Model, simplest first**: a run-rate extrapolation for flat spend, a trend over a recent window for steady growth,
   then a seasonal time-series model only where history shows seasonality. Keep the model rolling, so it is refreshed
   on a regular cadence.
4. **Overlay known changes**: planned launches, migrations, rate optimisation and commitment-based discounts, and
   usage optimisation opportunities.
5. **Agree variance thresholds** with the forecast owners (the Framework says each organisation defines its
   acceptable variance) and notify stakeholders when a threshold is exceeded or budget overspend is likely.
6. **Hand the forecast to Budgeting**, and have the forecast owner seek additional funding when actuals are
   expected to exceed it.

## Measuring the forecast
The Framework lists these KPIs:
- Forecast Accuracy Rate (Spend): (forecasted minus actual) divided by forecasted public cloud spend, over a period
  such as day, month or quarter.
- Forecast Drift Rate: (new forecast minus previous forecast) divided by the previous forecast.

## Gotchas
- A trend extrapolated through a recent step change (a new product) will mislead; use a driver-based model for that scope.
- Forecast at allocation-construct level, not per resource.

## Verify
- [ ] Forecast basis is amortised, discount-adjusted usage and the cleaning of one-offs is documented.
- [ ] Variance threshold and notification route are agreed with the forecast owner.

## Checked
Confirmed on the FinOps Framework Forecasting capability page (read in full): maturity stages (rolling and
trend-based at Walk; rolling, trend-based and driver-based at Run; discount-adjusted amortised usage; rate and usage
optimisation included), variance thresholds and notifications, hand-off to Budgeting, forecast owner seeking funding,
the Forecast Accuracy Rate (Spend) and Forecast Drift Rate formulas. Removed: history length, 30-day run-rate and
3-6 month windows, BigQuery ML ARIMA_PLUS, Prophet and statsmodels, native Cost Explorer, Azure and GCP forecast
claims, P10/P50/P90 ranges, backtest target, and two cited sources that could not be read.
Method: docs-checked 2026-11-09 against finops.org Framework Forecasting capability page
