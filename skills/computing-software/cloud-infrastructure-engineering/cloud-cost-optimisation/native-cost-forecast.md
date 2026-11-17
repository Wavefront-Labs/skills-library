---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.native-cost-forecast
name: native-cost-forecast
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, forecasting, native-cost-forecast, aws-cost-explorer, azure-cost-management, google-cloud-billing, native-cost-tools]
level: intro
status: docs-checked
description: "Use native forecast features in AWS Cost Explorer, Azure Cost Analysis and Google Cloud Billing reports: what they model, prediction intervals and when to go custom."
sources:
  - https://docs.aws.amazon.com/cost-management/latest/userguide/ce-forecast.html
  - https://learn.microsoft.com/azure/cost-management-billing/costs/cost-analysis-common-uses
  - https://docs.cloud.google.com/billing/docs/reports
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native forecast features and their limits

Provider forecasts are one click away and fine for a Crawl-stage practice or a quick
projection. Know what they do before quoting them.

## What each offers
- **AWS Cost Explorer**: you create a forecast by selecting a future time range for a report.
  It is based on past usage and shown on line and bar charts with an 80% prediction interval.
  If AWS lacks the data for an 80% interval (common for accounts with under one full billing
  cycle) no forecast is shown. With consolidated billing the forecast uses data from all
  accounts, but a newly added member account is not included until its spending pattern has
  been analysed. Discounts are included by default; the page suggests **Show net unblended
  costs** if you want non-recurring discounts such as refunds included.
- **Azure Cost Management**: Cost Analysis shows forecast cost on area and stacked column
  charts, based on historical resource use. The forecast is projected for the **Total**; it is
  not calculated per service or per resource when you group by them.
- **Google Cloud Billing**: the billing reports page mentions forecasted future costs based
  on historical trends in the billing report section.

## When native is enough
- Projection for a stable scope.
- Quick sanity check against a custom forecast.

## Limits
- Single provider only; no cross-cloud or SaaS totals.
- Based on history only (AWS: "based on your past usage"; Azure: "changes to your resource
  use affect forecast costs"), so it cannot know about planned launches or migrations.
- AWS and Azure forecasts are estimates that may differ from actual charges.
- Azure forecast is for the total only, so per-service forecasts must be built separately.
- Short history gives no AWS forecast at all.

## Steps
1. Record the native forecast weekly next to your own; compare accuracy.
2. Move to custom (trend or driver-based) when you need multi-cloud totals, business drivers,
   or an auditable forecast for finance.

## Gotchas
- State the forecast basis (metric, filters, whether discounts are included) whenever a
  native number is quoted.

## Verify
- [ ] The forecast basis is stated whenever a native number is quoted.

## Checked
Method: docs-checked 2026-11-09 against the AWS Cost Explorer forecasting page, the Azure common cost analysis uses page (forecast sections) and the Google Cloud billing reports page; read via summarising fetch. Dropped unconfirmed: 12-18 month horizon, ML basis, CLI example, forecast-based budget alerts on all three clouds, month-end/year-end Google forecast, amortised-metric and credits gotchas, and the FinOps Foundation source (not read).
