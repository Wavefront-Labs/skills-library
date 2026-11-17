---
id: computing-software.cloud-infrastructure-engineering.aws.cost-explorer-forecasting
name: cost-explorer-forecasting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cost-explorer, cost-forecast, get-cost-forecast, prediction-interval, finops, budget-planning]
level: practitioner
status: docs-checked
description: "Forecast AWS spend with Cost Explorer and get-cost-forecast, prediction intervals, filters per account or service, and when forecasts mislead (new workloads, commitments)."
sources: ["https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostForecast.html", "https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetUsageForecast.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost Explorer forecasting

## API
```bash
aws ce get-cost-forecast \
  --time-period Start=<START_DATE>,End=<END_DATE> \
  --metric AMORTIZED_COST --granularity MONTHLY --prediction-interval-level 80 \
  --filter '{"Dimensions":{"Key":"LINKED_ACCOUNT","Values":["<ACCOUNT_ID>"]}}'
aws ce get-usage-forecast --time-period Start=<START_DATE>,End=<END_DATE> \
  --metric USAGE_QUANTITY --granularity MONTHLY \
  --filter '{"Dimensions":{"Key":"USAGE_TYPE","Values":["<USAGE_TYPE>"]}}'
```
- `get-cost-forecast` predicts spend over the period based on your past costs; `get-usage-forecast`
  does the same for usage (metrics `USAGE_QUANTITY` or `NORMALIZED_USAGE_AMOUNT`).
- Cost metrics: `AMORTIZED_COST`, `BLENDED_COST`, `NET_AMORTIZED_COST`, `NET_UNBLENDED_COST`, `UNBLENDED_COST`.
- Granularity is `DAILY` or `MONTHLY` only (the enum also lists `HOURLY`, but the forecast operations do not
  support it): you can get 3 months of daily forecasts or 18 months of monthly forecasts.
- `--prediction-interval-level` is 51 to 99. Report the interval, not just the mean.
- The start date is included in the period and the end date is not.
- Filters take `Dimensions` such as `LINKED_ACCOUNT`, `SERVICE`, `REGION`, `USAGE_TYPE`, `INSTANCE_TYPE`, plus `Tags`
  and `CostCategories`, combined with `And`, `Or` and `Not`.

## How to use forecasts
- Monthly: forecast per business unit (cost category) vs budget; investigate where forecast > budget.
- Annual planning: start from the forecast, then add known changes (new products, migrations, commitment
  purchases, price changes) explicitly in a spreadsheet; the forecast is based on past costs only.

## Verify
- [ ] Monthly report compares last month's forecast with actual; error tracked over time.

## Checked
2026-10-28: Confirmed against the Cost Explorer API Reference pages GetCostForecast and GetUsageForecast and the botocore ce model: past-cost basis, DAILY/MONTHLY only with 3 months daily and 18 months monthly, metric values for cost and usage forecasts, prediction interval 51 to 99, start inclusive and end exclusive, supported filter dimensions. The two forecast commands passed check_commands.py. Read end to end. Removed as unconfirmed: the console description, forecast budget alerts using the same engine, "start must be today or later", history-length advice, and the "when forecasts mislead" bullets about credits, upfront fees and commitments. Replaced the sample account ID and usage type with placeholders.

Method: documentation only; no commands were run.
