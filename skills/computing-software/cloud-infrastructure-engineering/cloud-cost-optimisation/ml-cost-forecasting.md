---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.ml-cost-forecasting
name: ml-cost-forecasting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, forecasting, ml-cost-forecasting, prophet, arima, time-series-forecasting, statistical-forecasting]
level: advanced
status: docs-checked
description: "Forecast cloud cost with statistical models: prepare the series, choose ETS or Prophet, add events and drivers, cross-validate, and report prediction intervals."
sources: ["https://facebook.github.io/prophet/docs/quick_start.html", "https://otexts.com/fpp3/", "https://www.finops.org/framework/capabilities/forecasting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Statistical and ML cost forecasting

Run-rate and linear trends break on seasonality, step changes and growth curves. Time-series models
handle those, if the input series is clean.

## Prepare the series
- Forecast discount-adjusted, amortised cost per forecast unit (BU, product, provider); the FinOps
  Run-level description tracks forecasts against discount-adjusted, amortised usage.
- Remove or flag one-offs (incidents, migrations, data backfills); add known future events as
  regressors or holidays.
- Commitment purchases, support and tax are best forecast separately as known schedules, so the
  model does not try to repeat their spikes.

## Models
- **ETS / Holt-Winters**: exponential smoothing with trend and seasonal components; a sensible
  baseline for smooth series (fpp3 exponential smoothing chapters).
- **ARIMA**: classical alternative covered in fpp3; compare it against ETS by back-test error.
- **Prophet**: trend changepoints plus seasonality and holidays, with extra regressors for business
  drivers. A regressor column must exist in both the fitting and the prediction dataframes, so you
  need a forecast of the driver itself:
  ```python
  from prophet import Prophet
  m = Prophet(yearly_seasonality=True, weekly_seasonality=True, changepoint_prior_scale=0.1)
  m.add_regressor('orders'); m.fit(df)        # df: ds, y, orders
  fc = m.predict(m.make_future_dataframe(90).merge(future_orders, on='ds'))
  ```
  `changepoint_prior_scale` defaults to 0.05; raising it makes the trend more flexible and lowering
  it makes it less flexible. A holidays dataframe must list occurrences in the past and in the
  forecast period; `holidays_prior_scale` (default 10) can be reduced if holiday effects overfit.
- **Driver-based** forecasting: the FinOps Run description combines rolling, trend-based and
  driver-based models. See `driver-based-forecasting`.

## Steps
1. Back-test: Prophet's `cross_validation` takes `initial`, `period` and `horizon`; by default the
   initial training period is three times the horizon. Compute error (MAPE is available from
   `performance_metrics`) per series and pick the model by out-of-sample error, not by fit.
2. Reconcile hierarchy: forecast per BU and sum to total (the bottom-up approach in the fpp3
   hierarchical chapter), and compare with a total-level forecast.
3. Publish the point forecast and a prediction interval (fpp3 shows 80% and 95% intervals); finance
   budgets on the point, risk on the upper band.
4. Retrain on a regular cadence and track forecast accuracy (see `forecast-accuracy`).

## Gotchas
- Org changes (team moves) create level shifts; restate history to the current mapping first.
- Models extrapolate trends; review long horizons with the owners.
- Forecast owners must seek funding when actuals exceed the forecast (FinOps Forecasting page).

## Verify
- [ ] Cross-validation error recorded per series and compared with a run-rate baseline.
- [ ] Forecasts include intervals and the training data cut-off date.

## Checked

Method: docs-checked 2026-11-09 against Prophet quick start, trend changepoints, seasonality/holidays/regressors and diagnostics docs (raw GitHub), fpp3 pages (exponential smoothing, prediction intervals, hierarchical forecasting) and the FinOps Forecasting capability page (read maturity and definition sections).
Removed as unconfirmed: BigQuery ML ARIMA_PLUS SQL and its claims (cloud.google.com unreadable), the "at least 1 year of data" rule, the "Usage rows only / EffectiveCost" column advice, the 90-day horizon and 80% interval prescriptions, the monthly retrain rule and the "better than run-rate baseline" threshold.
