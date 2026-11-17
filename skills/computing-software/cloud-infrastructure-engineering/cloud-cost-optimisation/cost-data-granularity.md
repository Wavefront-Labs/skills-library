---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-data-granularity
name: cost-data-granularity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, reporting-and-analytics, cost-data-granularity, data-retention, hourly-data, resource-level-data, cost-data-pipeline]
level: practitioner
status: draft
description: "Choose cost data granularity and history retention: hourly vs daily, resource-level vs aggregated, which uses need which, storage cost, and tiered retention."
sources: ["https://docs.aws.amazon.com/cur/latest/userguide/dataexports-create-standard.html", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/detailed-usage", "https://www.finops.org/framework/capabilities/reporting-analytics/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost data granularity and history retention

Hourly, resource-level billing data is big (tens to hundreds of GB per month for large estates).
Keep the detail where it earns its keep and aggregate the rest.

## What needs what
| Use | Time grain | Resource detail | History |
|---|---|---|---|
| Commitment sizing (RI/SP/CUD) | **hourly** | instance family / usage type | 30-90 days hourly |
| Anomaly detection | daily (hourly for fast detection) | service/account, resource for triage | 13 months daily |
| Rightsizing, idle detection | daily | **resource** | 30-90 days |
| Showback, chargeback | daily or monthly | owner/team | 3+ years monthly |
| Forecasting, seasonality | daily/monthly | team/service | 24-36 months |
| Audit / finance | monthly | invoice line | per records policy (often 7 years) |

## Provider options
- AWS Data Exports: time granularity hourly/daily/monthly; "include resource IDs" toggle; split cost
  allocation data for ECS/EKS adds rows.
- Google Cloud: standard vs **detailed usage cost** export (resource-level); both daily-partitioned.
- Azure: exports are daily-grain with resource IDs.

## Steps
1. Export at the finest grain you need anywhere (usually hourly + resource IDs) into cheap object
   storage.
2. Build tiers in the warehouse:
   - `raw_hourly_resource`: 90 days, partitioned by date.
   - `daily_resource`: 13 months.
   - `daily_team_service`: 3-5 years.
   - `monthly_invoice`: per records policy.
3. Set partition expiration / lifecycle rules so old detail ages out automatically
   (e.g. BigQuery `partition_expiration_days`, S3 lifecycle to Glacier for raw files).
4. Document in the data catalogue which table answers which question.

## Gotchas
- Dropping hourly too early blocks commitment analysis; keep at least 30 days hourly (60-90 is
  better for seasonality).
- Daily rollups must keep the cost basis columns (billed, effective, list) and charge category or
  they become useless for reconciliation.
- Raw files are the only way to rebuild after a mapping change; keep them in archive storage.

## Verify
- [ ] Each table has a documented grain, retention and owner.
- [ ] Storage cost of the FinOps data platform is itself tracked.
